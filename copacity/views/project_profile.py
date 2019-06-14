from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from copacity.models import Project
from copacity.models import Allocation, Holidays, Time_Off
from copacity.tables import Project_Resource_table
import datetime
from datetime import date, timedelta
from django.forms.models import model_to_dict
from copacity.forms import edit_resource_allocation
from django.http import HttpResponseRedirect
from django.db.models import Count, Min, Sum, Avg
import uuid
from django.contrib.auth.decorators import login_required

@login_required
#main definition for view.
def project_properties(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()

    # Main call to the DB for project data
    project = Project.objects.get(pk=offset)

    # Project Resource table
    table = Project_Resource_table(Allocation.objects.filter(project_id=offset).filter(active=True).order_by('user_id').distinct('user_id'))

#---------------------------------------
#---------------------------------------

    # Date ranges for the project allocation form / table 

    proj_obj = Project.objects.get(pk=offset)
    project_start = proj_obj.start_date
    project_end = proj_obj.end_date

    
    def find_second_range():
        start = project_start.weekday()
        count = 0
        if start == 0:
            count = 0
        else:
            while start !=6:
                start += 1
                count += 1
        return count

    def list_of_mondays(start, end):
        day_count = (end - start).days + 1
        count = 0
        mondays = []
        while count < day_count:
            if start.weekday() == 0:
                mondays.append(start)
            start += timedelta(days = 1)
            count += 1
        return mondays
        
    def create_date_range(date, end):
        friday = date + timedelta(days = 4)
        if friday < end:
            return date, friday
        else:
            return date, end
    
    def project_weeks():
        lst_mondays = list_of_mondays(project_start, project_end)
        count=0
        range_list =[]
        first_day = project_start
        first_friday_after_start = project_start + timedelta(days = find_second_range() - 2)
        if first_day <= first_friday_after_start:
            range_list.append(tuple((first_day, first_friday_after_start)))
        for i in lst_mondays:
            range_list.append(create_date_range(lst_mondays[count], project_end))
            count += 1
        return range_list
            
    display_ranges = project_weeks


#---------------------------------------
    
#---------------------------------------
    
    #Project Resource list for Resouce allocation


    def table_header():
        a = Allocation.objects.filter(project_id=offset).filter(active=True).order_by('user_id').distinct('user_id')
        th = []
        for i in a:
            th.append(i.user_id)
        return th
            
    project_resource_list = table_header()
    
    def resource_allocation_by_week(start, end):
        
        users_on_project = Allocation.objects.filter(project_id=offset).filter(active=True)
        users_in_date_range = users_on_project.filter(week__range=[start, end])
        dict_of_user_hours = {}
        for i in users_on_project:
            total_weeks_allo = 0
            for a in Allocation.objects.filter(week__range=[start, end]).filter(user_id=i.user_id).filter(active=True):
                total_weeks_allo += a.allocated_hours

            holidays = Holidays.objects.filter(holiday_date__range=[start, end]).aggregate(Sum('hours_lost')).values()
            time_off = Time_Off.objects.filter(date__range=[start, end]).filter(user_id=i.user_id).aggregate(Sum('hours_lost')).values()
            
            holidays_value = holidays[0]
            time_off_value = time_off[0]
    
            if holidays_value > 0 and time_off_value > 0:
                holiday_and_time_off = holidays_value + time_off_value
            elif holidays_value > 0 and not time_off_value > 0:
                holiday_and_time_off = holidays_value
            elif not holidays_value > 0 and time_off_value > 0:
                holiday_and_time_off = time_off_value
            else:
                holiday_and_time_off = 0

            avalible_total = i.user_id.weekly_copacity - total_weeks_allo - holiday_and_time_off

            allocated_by_date = users_in_date_range.filter(user_id=i.user_id).values_list('allocated_hours', flat=True)



            if users_in_date_range.filter(user_id=i.user_id).exists():
                Allocation_pk = users_in_date_range.filter(user_id=i.user_id).values_list('id', flat=True)            
                f_inst = Allocation.objects.get(pk=Allocation_pk[0])
                allocation_form = edit_resource_allocation(instance = f_inst, prefix = Allocation_pk)
                dict_of_user_hours[i.user_id] = (allocation_form.as_p, allocated_by_date[0], avalible_total)
                if request.method == 'POST':
                    allocation_form = edit_resource_allocation(request.POST, instance = f_inst, prefix = Allocation_pk)
                    if allocation_form.is_valid():
                        if allocation_form.has_changed():
                            allocation_form.save()

            else:
                unique_id = "%s%s" % (start, i.user_id)
                non_displayed_form_values = Allocation(
                    user_id = i.user_id,
                    project_id = i.project_id,
                    week = start,
                    actual_hours = 0,
                    )
                allocation_form_new = edit_resource_allocation(initial={'allocated_hours' : 0}, prefix = unique_id)
                dict_of_user_hours[i.user_id] = (allocation_form_new.as_p, 0, avalible_total)
                if request.method == 'POST':
                    allocation_form_new = edit_resource_allocation(request.POST, instance=non_displayed_form_values, prefix = unique_id)
                    if allocation_form_new.is_valid():
                        if allocation_form_new.has_changed():
                            allocation_form_new.save()
                            

        return dict_of_user_hours
        
            
    # def final_resource_allo_grid():
    #     dict_of_stuff = []
    #     for i in display_ranges():
    #         a = resource_allocation_by_week(i[0],i[1])
    #         dict_of_stuff.append(tuple((i[0],i[1],a)))
    #     return dict_of_stuff
    

    
    # resource_allocation_grid = final_resource_allo_grid
    
    
    dict_of_stuff = []
    for i in display_ranges():
        a = resource_allocation_by_week(i[0],i[1])
        dict_of_stuff.append(tuple((i[0],i[1],a)))
    
        
    resource_allocation_grid = dict_of_stuff
    
    if request.method == 'POST':
        return HttpResponseRedirect('/project_profile/%s/' % offset)
        
    
    # if test == 0:
    #     return HttpResponseRedirect('/project_list/')
    # return HttpResponseRedirect('/project_list/')

    

#---------------------------------------
#---------------------------------------

    # form set test 
    # testformset = formset_factory(edit_resource_allocation, extra=25)


    return render(request, '../templates/copacity/project_profile.html', {
        'project_name': project.project_name,
        'project_type': project.project_type,
        'project_scope_PM': project.pm_scope,
        'project_scope_DEV': project.dev_scope,
        'project_scope_DESIGN': project.design_scope,
        'project_scope_TESTING': project.testing_scope,
        'project_date_Created': project.created_date,
        'project_date_Start': project.start_date,
        'project_date_End': project.end_date,
        'table': table,
        # 'display_ranges': display_ranges,
        'project_resource_list': project_resource_list,
        'project_id': offset,
        'resource_allocation_grid' : resource_allocation_grid,
        # 'testformset' : testformset
        })


    