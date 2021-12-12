from django.urls import include, path, re_path
from django.conf import settings
from cabot.cabotapp.views import (
    about, run_status_check, graphite_api_data, checks_run_recently,
    duplicate_icmp_check, duplicate_graphite_check, duplicate_http_check, duplicate_jenkins_check,
    duplicate_instance, acknowledge_alert, remove_acknowledgement,
    GraphiteCheckCreateView, GraphiteCheckUpdateView,
    HttpCheckCreateView, HttpCheckUpdateView,
    ICMPCheckCreateView, ICMPCheckUpdateView,
    JenkinsCheckCreateView, JenkinsCheckUpdateView,
    StatusCheckDeleteView, StatusCheckListView, StatusCheckDetailView,
    StatusCheckResultDetailView, StatusCheckReportView, UserProfileUpdateAlert,
    PluginSettingsView, AlertTestView, AlertTestPluginView, SetupView, OnCallView)

from cabot.cabotapp.views import (InstanceListView, InstanceDetailView,
                                  InstanceUpdateView, InstanceCreateView, InstanceDeleteView,
                                  ServiceListView, ServicePublicListView, ServiceDetailView,
                                  ServiceUpdateView, ServiceCreateView, ServiceDeleteView,
                                  UserProfileUpdateView, ShiftListView, subscriptions)

from cabot.cabotapp.utils import cabot_needs_setup

from cabot import rest_urls
from rest_framework.documentation import include_docs_urls

from django.contrib import admin
from django.views.generic.base import RedirectView
from django.views.static import serve
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView

admin.autodiscover()

from importlib import import_module
import logging
import os

logger = logging.getLogger(__name__)


def first_time_setup_wrapper(func):
    def wrapper(*args, **kwargs):
        if cabot_needs_setup():
            return redirect('first_time_setup')
        else:
            return func(*args, **kwargs)

    return wrapper


def home_authentication_switcher(request, *args, **kwargs):
    if cabot_needs_setup():
        return redirect('first_time_setup')
    if not request.user.is_authenticated:
        return ServicePublicListView.as_view()(request, *args, **kwargs)
    else:
        return ServiceListView.as_view()(request, *args, **kwargs)


urlpatterns = [
    # for the password reset views
    re_path('^', include('django.contrib.auth.urls')),

    re_path(r'^(?P<path>favicon\.ico)$', serve, name='favicon',
         kwargs={'document_root': os.path.join(settings.STATIC_ROOT, 'arachnys/img')}),

    re_path(r'^$', view=home_authentication_switcher,
         name='dashboard'),
    re_path(r'^subscriptions/', view=subscriptions,
         name='subscriptions'),
    re_path(r'^accounts/login/', view=first_time_setup_wrapper(LoginView.as_view()), name='login'),
    re_path(r'^accounts/logout/', view=LogoutView.as_view(), name='logout'),
    re_path(r'^setup/', view=SetupView.as_view(), name='first_time_setup'),
    re_path(r'^accounts/password-reset/',
         view=PasswordResetView.as_view(), name='password-reset'),
    re_path(r'^accounts/password-reset-done/',
         view=PasswordResetDoneView.as_view(), name='password-reset-done'),
    re_path(r'^accounts/password-reset-confirm/',
         view=PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    re_path(r'^status/', view=checks_run_recently,
         name='system-status'),
    re_path(r'^about/', view=about,
         name='about-cabot'),

    re_path(r'^services/', view=ServiceListView.as_view(),
         name='services'),
    re_path(r'^public/', view=ServicePublicListView.as_view(),
         name='public'),
    re_path(r'^service/create/', view=ServiceCreateView.as_view(),
         name='create-service'),
    re_path(r'^service/update/(?P<pk>\d+)/',
         view=ServiceUpdateView.as_view(), name='update-service'),
    re_path(r'^service/delete/(?P<pk>\d+)/',
         view=ServiceDeleteView.as_view(), name='delete-service'),
    re_path(r'^service/(?P<pk>\d+)/',
         view=ServiceDetailView.as_view(), name='service'),
    re_path(r'^service/acknowledge_alert/(?P<pk>\d+)/',
         view=acknowledge_alert, name='acknowledge-alert'),
    re_path(r'^service/remove_acknowledgement/(?P<pk>\d+)/',
         view=remove_acknowledgement, name='remove-acknowledgement'),

    re_path(r'^instances/', view=InstanceListView.as_view(),
         name='instances'),
    re_path(r'^instance/create/', view=InstanceCreateView.as_view(),
         name='create-instance'),
    re_path(r'^instance/update/(?P<pk>\d+)/',
         view=InstanceUpdateView.as_view(), name='update-instance'),
    re_path(r'^instance/duplicate/(?P<pk>\d+)/',
         view=duplicate_instance, name='duplicate-instance'),
    re_path(r'^instance/delete/(?P<pk>\d+)/',
         view=InstanceDeleteView.as_view(), name='delete-instance'),
    re_path(r'^instance/(?P<pk>\d+)/',
         view=InstanceDetailView.as_view(), name='instance'),

    re_path(r'^checks/$', view=StatusCheckListView.as_view(),
         name='checks'),
    re_path(r'^check/run/(?P<pk>\d+)/',
         view=run_status_check, name='run-check'),
    re_path(r'^check/delete/(?P<pk>\d+)/',
         view=StatusCheckDeleteView.as_view(), name='delete-check'),
    re_path(r'^check/(?P<pk>\d+)/',
         view=StatusCheckDetailView.as_view(), name='check'),
    re_path(r'^checks/report/$',
         view=StatusCheckReportView.as_view(), name='checks-report'),

    re_path(r'^icmpcheck/create/', view=ICMPCheckCreateView.as_view(),
         name='create-icmp-check'),
    re_path(r'^icmpcheck/update/(?P<pk>\d+)/',
         view=ICMPCheckUpdateView.as_view(), name='update-icmp-check'),
    re_path(r'^icmpcheck/duplicate/(?P<pk>\d+)/',
         view=duplicate_icmp_check, name='duplicate-icmp-check'),
    re_path(r'^graphitecheck/create/',
         view=GraphiteCheckCreateView.as_view(), name='create-graphite-check'),
    re_path(r'^graphitecheck/update/(?P<pk>\d+)/',
         view=GraphiteCheckUpdateView.as_view(), name='update-graphite-check'),
    re_path(r'^graphitecheck/duplicate/(?P<pk>\d+)/',
         view=duplicate_graphite_check, name='duplicate-graphite-check'),
    re_path(r'^httpcheck/create/', view=HttpCheckCreateView.as_view(),
         name='create-http-check'),
    re_path(r'^httpcheck/update/(?P<pk>\d+)/',
         view=HttpCheckUpdateView.as_view(), name='update-http-check'),
    re_path(r'^httpcheck/duplicate/(?P<pk>\d+)/',
         view=duplicate_http_check, name='duplicate-http-check'),
    re_path(r'^jenkins_check/create/', view=JenkinsCheckCreateView.as_view(),
         name='create-jenkins-check'),
    re_path(r'^jenkins_check/update/(?P<pk>\d+)/',
         view=JenkinsCheckUpdateView.as_view(), name='update-jenkins-check'),
    re_path(r'^jenkins_check/duplicate/(?P<pk>\d+)/',
         view=duplicate_jenkins_check,
         name='duplicate-jenkins-check'),

    re_path(r'^result/(?P<pk>\d+)/',
         view=StatusCheckResultDetailView.as_view(), name='result'),
    re_path(r'^shifts/', view=ShiftListView.as_view(),
         name='shifts'),
    re_path(r'^graphite/', view=graphite_api_data,
         name='graphite-data'),
    re_path(r'^user/(?P<pk>\d+)/profile/$',
         view=UserProfileUpdateView.as_view(), name='user-profile'),
    re_path(r'^alert-test/$',
         view=AlertTestView.as_view(), name='alert-test'),
    re_path(r'^alert-test-plugin/$',
         view=AlertTestPluginView.as_view(), name='alert-test-plugin'),
    re_path(r'^plugin-settings/$',
         view=RedirectView.as_view(url='global/', permanent=False), name='plugin-settings-global'),
    re_path(r'^plugin-settings/(?P<plugin_name>.+)/$',
         view=PluginSettingsView.as_view(), name='plugin-settings'),
    re_path(r'^user/(?P<pk>\d+)/profile/(?P<alerttype>.+)/',
         view=UserProfileUpdateAlert.as_view(), name='update-alert-user-data'),
    re_path(r'^admin/', admin.site.urls),
    # Comment below line to disable browsable rest api
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^api/', include(rest_urls.router.urls)),
    re_path(r'^api/oncall', view=OnCallView.as_view(), name='oncall'),
    re_path(r'^docs/',
         include_docs_urls(title="Cabot API", description="An API to create and view Cabot checks and services."))
]


def append_plugin_urls():
    """
    Appends plugin specific URLs to the urlpatterns variable.
    """
    global urlpatterns
    for plugin in settings.CABOT_PLUGINS_ENABLED_PARSED:
        try:
            _module = import_module('%s.urls' % plugin)
        except ImportError:
            pass
        else:
            urlpatterns += [
                path(r'^plugins/%s/' % plugin, include('%s.urls' % plugin))
            ]


append_plugin_urls()

if settings.AUTH_SOCIAL:
    urlpatterns += [
        path('', include('social_django.urls', namespace='social'))
    ]

if settings.URL_PREFIX.strip('/'):
    urlpatterns = [
        path(r'^%s/' % settings.URL_PREFIX.strip('/'), include(urlpatterns))
    ]
