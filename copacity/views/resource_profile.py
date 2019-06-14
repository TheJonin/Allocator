from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from copacity.models import Resource, Schedule, Time_Off, Allocation, Holidays
import datetime
from datetime import date
from copacity.tables import project_list_by_user
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

@login_required
def resource_profile(request, resource_id):
    resource = Resource.objects.get(pk=resource_id)
    
    
# -----------------------------  

    def h_and_t(start, end):
        holidays = Holidays.objects.filter(holiday_date__range=[start, end]).aggregate(Sum('hours_lost')).values()
        time_off = Time_Off.objects.filter(date__range=[start, end]).filter(user_id=resource_id).aggregate(Sum('hours_lost')).values()
                
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
        
        return holiday_and_time_off

        
    def filtered_total(start, end):
        queryset = Allocation.objects.filter(week__range=[start, end]).filter(user_id=resource_id).filter(active=True).aggregate(Sum('allocated_hours')).values()
        value = queryset[0]
        if value is None:
            value=0
        return value
        
        
    def this_week():
        lst = []
        today = datetime.date.today()
        last_monday = today - datetime.timedelta(days=today.weekday()) 
        start = last_monday
        end = last_monday + datetime.timedelta(6)
        allocated = filtered_total(start, end)
        avalible = resource.weekly_copacity - h_and_t(start, end)
        percentage = 100* allocated / (float(resource.weekly_copacity) - h_and_t(start, end))
        percentage_formated = '%s%s' % (int(round(percentage)), '%')
        lst.extend((avalible, allocated, percentage_formated))
        return lst
        
    def next_week():
        lst = []
        today = datetime.date.today()
        last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1) 
        start = last_monday
        end = last_monday + datetime.timedelta(6)
        allocated = filtered_total(start, end)
        avalible = resource.weekly_copacity - h_and_t(start, end)
        percentage = 100* allocated / (float(resource.weekly_copacity) - h_and_t(start, end))
        percentage_formated = '%s%s' % (int(round(percentage)), '%')
        lst.extend((avalible, allocated, percentage_formated))
        return lst
        
    def thirty_days():
        lst = []
        first_day = datetime.date.today()
        last_day = first_day + datetime.timedelta(30)
        start = first_day
        end = last_day
        allocated = filtered_total(start, end)
        avalible = (resource.weekly_copacity*4) - h_and_t(start, end)
        percentage = 100* allocated / (float(resource.weekly_copacity*4) - h_and_t(start, end))
        percentage_formated = '%s%s' % (int(round(percentage)), '%')
        lst.extend((avalible, allocated, percentage_formated))
        return lst
        
    def sixty_days():
        lst = []
        first_day = datetime.date.today()
        last_day = first_day + datetime.timedelta(60)
        start = first_day
        end = last_day
        allocated = filtered_total(start, end)
        avalible = (resource.weekly_copacity*8) - h_and_t(start, end)
        percentage = 100* allocated / (float(resource.weekly_copacity*8) - h_and_t(start, end))
        percentage_formated = '%s%s' % (int(round(percentage)), '%')
        lst.extend((avalible, allocated, percentage_formated))
        return lst

    def ninty_days():
        lst = []
        first_day = datetime.date.today()
        last_day = first_day + datetime.timedelta(90)
        start = first_day
        end = last_day
        allocated = filtered_total(start, end)
        avalible = (resource.weekly_copacity*12) - h_and_t(start, end)
        percentage = 100* allocated / (float(resource.weekly_copacity*12) - h_and_t(start, end))
        percentage_formated = '%s%s' % (int(round(percentage)), '%')
        lst.extend((avalible, allocated, percentage_formated))
        return lst



    this_week = this_week
    next_week = next_week
    thirty_days = thirty_days
    sixty_days = sixty_days
    ninty_days = ninty_days
    
# ---------------------------------

    
    def schedule():
        schedule = Schedule.objects.filter(user_id=resource_id).order_by('day')
        schedule_lst = []
        for i in schedule:
            schedule_lst.append('%s - %s to %s with %s' % (i.day.day_name, i.get_start_time_display(), i.get_end_time_display(), i.lunch))
        return schedule_lst
            
    schedule_table = schedule
    
    def time_off():
        time_off = Time_Off.objects.filter(user_id=resource_id).order_by('date')
        time_off_lst = []
        for i in time_off:
            if i.date > datetime.date.today():
                time_off_lst.append('%s - %s Hours' % (i.date, i.hours_lost))
        return time_off_lst
        
    
    time_off_table = time_off
    check_len = len(time_off_table())
    if check_len > 4:
        more = "more..."
    else:
        more = ""
    
    

    table2 = project_list_by_user(Allocation.objects.filter(user_id=resource_id).filter(project_id__end_date__gte=date.today()).distinct('project_id'), prefix="projects")

    
    
    return render(request, '../templates/copacity/resource_profile.html', {
        'name': resource.resource_name,
        'type': resource.resource_type,
        'copacity': resource.weekly_copacity,
        'schedule': schedule_table,
        'time_off': time_off_table,
        'table2': table2,
        'this_week': this_week,
        'next_week': next_week,
        'thirty_days': thirty_days,
        'sixty_days': sixty_days,
        'ninty_days': ninty_days,
        'resource_id': resource_id,
        'more': more
        })
