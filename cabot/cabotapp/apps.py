import os

from django.apps import AppConfig
from django.db.models.signals import post_migrate

from cabot.celery import app

running_workers = dict()


def post_migrate_callback(**kwargs):
    from cabot.cabotapp.alert import update_alert_plugins
    from cabot.cabotapp.models import create_default_jenkins_config

    update_alert_plugins()
    create_default_jenkins_config()


class CabotappConfig(AppConfig):
    name = "cabot.cabotapp"

    def ready(self):
        post_migrate.connect(post_migrate_callback, sender=self)

        # Only run in application server context
        is_running_in_server_context = bool(os.environ.get("IS_WEBSERVER", False))
        if is_running_in_server_context:
            print(">>>> Registering events")

            def announce_worker_online(event):
                print(f"announce_worker_online {event}")
                running_workers[event["hostname"]] = event
                print(f"Add {running_workers}")

            def announce_worker_offline(event):
                print(f"announce_worker_offline {event}")
                event["hostname"] in running_workers and running_workers.pop(
                    event["hostname"]
                )
                print(f"Remove {running_workers}")

            with app.connection() as connection:
                recv = app.events.Receiver(
                    connection,
                    handlers={
                        "worker-online": announce_worker_online,
                        "worker-offline": announce_worker_offline,
                    },
                )
                recv.capture(limit=None, timeout=None, wakeup=True)
