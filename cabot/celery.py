import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cabot.settings")

app = Celery("cabot")
app.config_from_object("cabot.celeryconfig")
app.autodiscover_tasks()

running_workers = dict()

app.conf.beat_schedule = {
    "run-all-checks": {
        "task": "cabot.cabotapp.tasks.run_all_checks",
        "schedule": timedelta(seconds=60),
    },
    "update-shifts": {
        "task": "cabot.cabotapp.tasks.update_shifts",
        "schedule": timedelta(seconds=1800),
    },
    "clean-db": {
        "task": "cabot.cabotapp.tasks.clean_db",
        "schedule": timedelta(seconds=60 * 60 * 24),
    },
}
"""
# Only run in application server context
is_running_in_server_context = bool(os.environ.get("IS_WEBSERVER", False))

if is_running_in_server_context:
    state = app.events.State()

    def announce_worker_online(event):
        print(f"announce_worker_online {event}")
        running_workers[event["hostname"]] = event
        print(f"Add {running_workers}")

    def announce_worker_offline(event):
        print(f"announce_worker_offline {event}")
        event["hostname"] in running_workers and running_workers.pop(event["hostname"])
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
"""
