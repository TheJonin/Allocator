import django_tables2 as tables
from copacity.models import Project
from copacity.models import Resource
from copacity.models import Allocation
from django_tables2.utils import A
from django.contrib.auth.models import User




class Project_table(tables.Table):
    project_name = tables.LinkColumn('project_properties', args=[A('pk')])
    total_scope_column = tables.Column(accessor='total_scope', verbose_name='Allocation')
    
    class Meta:
        model = Project
        exclude = ('id', 'created_date', 'testing_scope')
        sequence = ('project_name', 'project_type',  'total_scope_column', 'pm_scope', 'dev_scope', 'design_scope')
        orderable = False
        attrs = {'class': 'table'}



class copacity_table(tables.Table):
    resource_name = tables.LinkColumn('resource_profile', args=[A('pk')])
    this_week = tables.Column(accessor='this_week')
    next_week = tables.Column(accessor='next_week')
    thirty_days = tables.Column(accessor='thirty_days')
    sixty_days = tables.Column(accessor='sixty_days')
    ninety_days = tables.Column(accessor='ninety_days')
    

    class Meta:
        model = Resource
        exclude = ('user', 'id', 'active', 'email_address', 'weekly_copacity', 'user_type')
        orderable = False
        attrs = {'class': 'table'}



# on the Project profile ths is the resource summary table        
class Project_Resource_table(tables.Table):
    role = tables.Column(accessor='user_id.resource_type')
    name = tables.Column(accessor='user_id.resource_name')
    allocation = tables.Column(accessor='return_allocation')


    class Meta:
        model = Allocation
        exclude = ('id', 'user_id', 'project_id', 'week', 'allocated_hours', 'actual_hours','active','actual', 'overage')
        orderable = False
        sequence = ('role', 'name', 'allocation', )
        attrs = {'class': 'table'}



class project_list_by_user(tables.Table):
    # project_name = tables.LinkColumn('project_profile', args=[A('pk')])
    project_name = tables.Column(accessor='project_id')
    this_week = tables.Column(accessor='this_week')
    total_left = tables.Column(accessor='total_left')
    total_allocated = tables.Column(accessor='return_allocation')
    first_allocated = tables.Column(accessor='first_allo_date')
    last_allocated = tables.Column(accessor='last_allo_date')

    class Meta:
        model = Allocation
        exclude = ('id','active', 'user_id', 'project_id', 'week', 'allocated_hours', 'actual_hours')
        sequence = ()
        orderable = False
        attrs = {'class': 'table'}
        

class managers_table(tables.Table):
    username = tables.LinkColumn('edit_manager', args=[A('pk')])
    email = tables.Column(accessor='email')
    last_login = tables.Column(accessor='last_login')
    date_joined = tables.Column(accessor='date_joined')

    
    class Meta:
        model = User
        exclude = ('id', 'first_name','last_name', 'password', 'groups', 'user_permissions', 'is_staff', 'is_superuser')
        orderable = False
        sequence = ('username', 'email', 'last_login', 'date_joined', 'is_active')
        attrs = {'class': 'table'}
