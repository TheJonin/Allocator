from django.conf.urls import url
from copacity.views.project_profile import project_properties
from copacity.views.project_list import project_list
from copacity.views.project_list_past import project_list_past
from copacity.views.project_list_all import project_list_all
from copacity.views.edit_project import edit_project
from copacity.views.edit_project_resource import edit_project_resource
from copacity.views.copacity_list import copacity_list
from copacity.views.copacity_list_inactive import copacity_list_inactive
from copacity.views.resource_profile import resource_profile
from copacity.views.edit_resource import edit_resource
from copacity.views.edit_schedule import edit_schedule
from copacity.views.edit_timeoff import edit_timeoff
from copacity.views.edit_timeoff_past import edit_timeoff_past
from copacity.views.resource_project_list import resource_project_list
from copacity.views.resource_project_list_past import resource_project_list_past
from copacity.views.resource_project_list_all import resource_project_list_all
from copacity.views.settings import settings
from copacity.views.new_project import new_project
from copacity.views.new_resource import new_resource
from copacity.views.settings_holiday import settings_holiday
from copacity.views.settings_holiday_past import settings_holiday_past
from copacity.views.settings_project_type import settings_project_type
from copacity.views.settings_resource_type import settings_resource_type
from copacity.views.settings_work_days import settings_work_days
from copacity.views.users import users
from copacity.views.users_inactive import users_inactive
from copacity.views.new_manager import new_manager
from copacity.views.edit_manager import edit_manager
from copacity.views.login_success import login_success


urlpatterns = [
    url(r'^project_profile/$', project_properties),
    url(r'^project_list/$', project_list, name="project_list"),
    url(r'^project_list_past/$', project_list_past, name="project_list_past"),
    url(r'^project_list_all/$', project_list_all, name="project_list_all"),
    url(r'^project_profile/(\d+)/$', project_properties, name='project_properties'),
    url(r'^edit_project/(\d+)/$', edit_project, name='edit_project'),
    url(r'^edit_project_resource/(\d+)/$', edit_project_resource, name='edit_project_resource'),
    url(r'^copacity_list/$', copacity_list, name='copacity_list'),
    url(r'^copacity_list_inactive/$', copacity_list_inactive, name='copacity_list_inactive'),
    url(r'^resource_profile/(\d+)/$', resource_profile, name='resource_profile'),
    url(r'^edit_resource/(\d+)/$', edit_resource, name='edit_resource'),
    url(r'^edit_schedule/(\d+)/$', edit_schedule, name='edit_schedule'),
    url(r'^edit_timeoff/(\d+)/$', edit_timeoff, name='edit_timeoff'),
    url(r'^edit_timeoff_past/(\d+)/$', edit_timeoff_past, name='edit_timeoff_past'),
    url(r'^resource_project_list/(\d+)/$', resource_project_list, name='resource_project_list'),
    url(r'^resource_project_list_past/(\d+)/$', resource_project_list_past, name='resource_project_list_past'),
    url(r'^resource_project_list_all/(\d+)/$', resource_project_list_all, name='resource_project_list_all'),
    url(r'^settings/$', settings, name='settings'),
    url(r'^new_project/$', new_project, name='new_project'),
    url(r'^new_resource/$', new_resource, name='new_resource'),
    url(r'^settings_holiday/$', settings_holiday, name='settings_holiday'),
    url(r'^settings_holiday_past/$', settings_holiday_past, name='settings_holiday_past'),
    url(r'^settings_project_type/$', settings_project_type, name='settings_project_type'),
    url(r'^settings_resource_type/$', settings_resource_type, name='settings_resource_type'),
    url(r'^settings_work_days/$', settings_work_days, name='settings_work_days'),
    url(r'^users/$', users, name='users'),
    url(r'^users_inactive/$', users_inactive, name='users_inactive'),
    url(r'^new_manager/$', new_manager, name='new_manager'),
    url(r'^edit_manager/(\d+)/$', edit_manager, name='edit_manager'),
    url(r'login_success/$', login_success, name='login_success'),
]


