import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cabot.settings")

    from django.core.management import execute_from_command_line
    from .celery import register_events

    register_events()
    execute_from_command_line(sys.argv)
