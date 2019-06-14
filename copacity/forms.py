from django import forms
from django.forms import ModelForm, Textarea
from copacity.models import Project, Allocation, Resource, Schedule, Time_Off, User_Type, Project_Type, Resource_Type, Workdays, Holidays
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from bootstrap_datepicker.widgets import DatePicker
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget
import datetime
from django.core.exceptions import ValidationError
from allocator import settings


class edit_project_info(ModelForm):
    project_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    project_type = forms.ModelChoiceField(queryset=Project_Type.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    start_date = forms.DateField(widget=DateWidget(attrs={'class':'form-control', 'id':"yourdatetimeid",'name':"start_date"}, options={"format": "mm/dd/yyyy"}))
    end_date = forms.DateField(widget=DateWidget(attrs={'class':'form-control', 'id':"yourdatetimeid",'name':"end_date"}, options={"format": "mm/dd/yyyy"}))
    pm_scope = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    dev_scope = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    design_scope = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    testing_scope = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))       

    class Meta:
        model = Project
        exclude = ['created_date', ]
        fields = ['project_name', 'project_type', 'start_date', 'end_date', 'pm_scope', 'dev_scope', 'design_scope', 'testing_scope']


class new_project_form(ModelForm):
    project_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Agency - Project Name'}))
    project_type = forms.ModelChoiceField(queryset=Project_Type.objects.all(), widget=forms.Select(attrs={'class':'form-control','placeholder':'Please Select'}))
    start_date = forms.DateField(widget=DateWidget(attrs={'class':'form-control', 'id':"yourdatetimeid",'name':"start_date",'placeholder':'MM/DD/YYY'}, options={"format": "mm/dd/yyyy"}))
    end_date = forms.DateField(widget=DateWidget(attrs={'class':'form-control', 'id':"yourdatetimeid",'name':"end_date",'placeholder':'MM/DD/YYY'}, options={"format": "mm/dd/yyyy"}))
    pm_scope = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'####'}))
    dev_scope = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'####'}))
    design_scope = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'####'}))
    testing_scope = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))       


    class Meta:
        model = Project
        exclude = ['created_date', ]
        fields = ['project_name', 'project_type', 'start_date', 'end_date', 'pm_scope', 'dev_scope', 'design_scope', 'testing_scope']


class edit_project_resource(ModelForm):
    class Meta:
        model = Project
        exclude = []

class edit_resource_allocation(ModelForm):
    allocated_hours = forms.IntegerField(label='', required=False, widget=forms.NumberInput(attrs={'class':'form-control-allocation'}))
    
    class Meta:
        model = Allocation
        exclude = ['user_id', 'project_id', 'week', 'actual_hours', 'active']
        
        
class remove_resource(forms.Form):
    active = forms.BooleanField(label_suffix='', label='', required=False)
    

class add_resource(forms.Form):
    active = forms.BooleanField(label_suffix='', label='', required=False)


class edit_resource_info(ModelForm):
    resource_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # active = models.BooleanField(default=True)
    email_address = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    weekly_copacity = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    resource_type = forms.ModelChoiceField(queryset=Resource_Type.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Resource
        fields = ['resource_name', 'email_address', 'resource_type', 'weekly_copacity', 'active']
        exclude=['user_type']
        
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count()>1:
            raise ValidationError("Username already exists")
        return username
        
class new_resource_form(ModelForm):
    resource_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'John Smith'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'JohnS'}))
    email_address = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'JSmith@portal.sc.gov'}))
    weekly_copacity = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'##'}))
    resource_type = forms.ModelChoiceField(queryset=Resource_Type.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Resource
        exclude = [ 'user_type']
        fields = ['resource_name', 'username', 'email_address', 'weekly_copacity', 'resource_type',]
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username


class time_off(ModelForm):
    date = forms.DateField(widget=DateWidget(attrs={'class':'form-control', 'id':"yourdatetimeid",'name':"date", 'placeholder':'MM/DD/YYY'}, options={"format": "mm/dd/yyyy"}))
    hours_lost = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'##'}))
    
    class Meta:
        model = Time_Off
        exclude=['user_id']
        fields = ['date', 'hours_lost']


class schedule_edit(ModelForm):
    # day = forms.ModelChoiceField(queryset=Workdays.objects.filter(active=True), widget=forms.Select(attrs={'class':'form-control'}))
    start_time = forms.ChoiceField(choices = Schedule.times, widget=forms.Select(attrs={'class':'form-control'}))
    end_time = forms.ChoiceField(choices = Schedule.times, widget=forms.Select(attrs={'class':'form-control'}))
    lunch = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Schedule
        exclude=['user_id', 'day']
        fields = [ 'start_time', 'end_time', 'lunch']


class project_type(ModelForm):
    project_type = forms.CharField(label='Add Project Type', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'CCP / Custom App / EPS'}))
    
    class Meta:
        model = Project_Type
        fields = ['project_type']
        
class resource_type(ModelForm):
    resource_type = forms.CharField(label='Add Resource Type', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Developer / Project Manager / Design'}))
    
    class Meta:
        model = Resource_Type
        fields = ['resource_type']
        
class holidays(ModelForm):
    holiday_name = forms.CharField(label='Add Holiday', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Christmas / Bowling Party / Charity Event'}))
    holiday_date = forms.DateField(widget=DateWidget(attrs={'class':'form-control', 'id':"yourdatetimeid",'name':"holiday_date", 'placeholder':'MM/DD/YYY'}, options={"format": "mm/dd/yyyy"}))
    hours_lost = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'#'}))
    
    
    class Meta:
        model = Holidays
        fields = ['holiday_name', 'holiday_date', 'hours_lost']

        
class holidays_delete(forms.Form):
    active = forms.ModelMultipleChoiceField(queryset = Holidays.objects.filter(holiday_date__gt=datetime.date.today()-datetime.timedelta(1)).order_by('holiday_date'), widget = forms.CheckboxSelectMultiple, required=False, label="")
        
class edit_project_actuals(ModelForm):
    actual_hours = forms.IntegerField(label='', required=False, widget=forms.NumberInput(attrs={'class':'form-control-allocation'}))
    
    class Meta:
        model = Allocation
        exclude = ['user_id', 'project_id', 'week', 'allocated_hours', 'active']
        
class new_manager_form(ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'JSmith'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'JSmith@portal.sc.gov'}))
    
    class Meta:
        model = User
        exclude = ('id', 'first_name', 'last_name', 'password', 'groups', 'user_permissions', 'is_staff', 'is_superuser', 'is_active')
        fields = ['username', 'email']
        
        
class edit_manager_info(ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'JSmith'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'JSmith@portal.sc.gov'}))
    is_active = forms.BooleanField(label_suffix='', label='Active', required=False)

    class Meta:
        model = User
        exclude = ('id', 'first_name', 'last_name', 'password', 'groups', 'user_permissions', 'is_staff', 'is_superuser')
        fields = ['username', 'email', 'is_active']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count()>1:
            raise ValidationError("Username already exists")
        return username