from django.contrib import admin
from .models import *


# Register your models here.


    

admin.site.register(Resource_Type)
admin.site.register(User_Type)
admin.site.register(Resource)
admin.site.register(Time_Off)
admin.site.register(Passwords)

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'day', 'start_time', 'end_time', 'lunch')

admin.site.register(Schedule, ScheduleAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'project_type')
    search_fields = ('project_name',)

admin.site.register(Project, ProjectAdmin)

admin.site.register(Project_Type)

class AllocationAdmin(admin.ModelAdmin):
     raw_id_fields = ('user_id', 'project_id')
     
admin.site.register(Allocation, AllocationAdmin)
admin.site.register(Holidays)
admin.site.register(Workdays)