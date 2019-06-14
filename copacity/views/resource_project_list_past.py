from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from copacity.models import Resource, Allocation, Project, Holidays, Time_Off
from datetime import date, timedelta
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from copacity.forms import edit_project_actuals

@login_required
def resource_project_list_past(request, resource_id):

    resource_name = Resource.objects.get(pk=resource_id)
    
    assigned_projects = Allocation.objects.filter(user_id=resource_id)
 
    # test = []
    # for a in assigned_projects:
    #     b = a.project_id.id
    #     test.append(b)
        

#----------------------------------------------
#start date range calculations
#---------------------------------------------

    def date_range_calc(project_id):    
        proj_obj = Project.objects.get(pk=project_id)
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
            
        return project_weeks()
 
#----------------------------------------------
#end date range calculations
#---------------------------------------------



    
    projects_dict = {}
    for p in assigned_projects.distinct('project_id'):
        if p.project_id.end_date < date.today():
            #need dictionary with entity names as keys and the values being a list of lists with table rows
            date_range = []
            display_ranges = date_range_calc(p.project_id.id)
            for i in display_ranges:
                proj_id = p.project_id.id
                holidays = Holidays.objects.filter(holiday_date__range=[i[0], i[1]]).aggregate(Sum('hours_lost')).values()
                time_off = Time_Off.objects.filter(date__range=[i[0], i[1]]).filter(user_id=resource_name.id).aggregate(Sum('hours_lost')).values()
                
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
                
                avalible_copacity = resource_name.weekly_copacity - holiday_and_time_off
                allocation = assigned_projects.filter(project_id=p.project_id.id).filter(active=True).filter(week__range=[i[0], i[1]]).aggregate(avalible_copacity=Coalesce(Sum('allocated_hours'),0)).values()
                percentage = '%s%s' % (((int(round(float(allocation[0]*100) / float(avalible_copacity))))), '%')
                actual = edit_project_actuals()
                date_list = [proj_id, i[0], i[1], avalible_copacity, allocation[0], percentage, actual]
                date_range.append(date_list)
            
            projects_dict[p.project_id.project_name] = [date_range]
            # projects_dict = display_ranges

    
    
    
    
    
    return render(request, '../templates/copacity/resource_project_list_past.html', {
        'resource_name': resource_name,
        'projects_dict':projects_dict,
        'resource_id':resource_id,
        # 'a':a,
        # 'test':test
        })
