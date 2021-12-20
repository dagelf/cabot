from datetime import timedelta

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def jenkins_human_url(jobname):
    return '{}job/{}/'.format(settings.JENKINS_API, jobname)


@register.simple_tag
def echo_setting(setting):
    return getattr(settings, setting, '')


@register.simple_tag
def is_app_installed(app):
    from django.apps import apps
    return apps.is_installed(app)


@register.filter(name='format_timedelta')
def format_timedelta(delta):
    # Getting rid of microseconds.
    return str(timedelta(days=delta.days, seconds=delta.seconds))


@register.filter
def for_service(objects, service):
    return objects.filter(service=service)


@register.filter
def all_status_check_by_ctype(instance, _polymorphic_ctype__model):
    return instance.status_check_by_ctype(_polymorphic_ctype__model + "statuscheck").all()