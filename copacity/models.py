from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.db.models import Sum, Max, Min
import datetime
import calendar
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User


# for resource   
class Resource_Type(models.Model):
    resource_type = models.CharField(max_length=15)

    def __str__(self):
        return self.resource_type

class User_Type(models.Model):
    user_type = models.CharField(max_length=15)
    
    def __str__(self):
        return self.user_type
    
class Resource(models.Model):
    user = models.ForeignKey(User, null=True, blank=True )
    resource_name = models.CharField(max_length=150, unique=True)
    active = models.BooleanField(default=True)
    email_address = models.EmailField()
    weekly_copacity = models.IntegerField()
    resource_type = models.ForeignKey(Resource_Type)
    user_type = models.ForeignKey(User_Type)
    
    def __str__(self):
        return self.resource_name
        
    #resource allocation calculations
    def filtered_total(self, start, end, num_weeks):
        allocation = Allocation.objects.filter(week__range=[start, end]).filter(user_id=self.id).filter(active=True).aggregate(Sum('allocated_hours')).values()
        holidays = Holidays.objects.filter(holiday_date__range=[start, end]).aggregate(Sum('hours_lost')).values()
        holidays_value = holidays[0]
        time_off = Time_Off.objects.filter(date__range=[start, end]).filter(user_id=self.id).aggregate(Sum('hours_lost')).values()
        time_off_value = time_off[0]

        if holidays_value > 0 and time_off_value > 0:
            holiday_and_time_off = holidays_value + time_off_value
        elif holidays_value > 0 and not time_off_value > 0:
            holiday_and_time_off = holidays_value
        elif not holidays_value > 0 and time_off_value > 0:
            holiday_and_time_off = time_off_value
        else:
            holiday_and_time_off = 0

        final_capacity = (self.weekly_copacity*num_weeks) - holiday_and_time_off

        copacity_percent_before_format = float(allocation[0])/final_capacity*100
        copacity_percent_formated = "%s%s" % (int(round(copacity_percent_before_format)), "%")
        return copacity_percent_formated
        
    def this_week(self):
        today = datetime.date.today()
        last_monday = today - datetime.timedelta(days=today.weekday()) 
        start = last_monday
        end = last_monday + datetime.timedelta(6)
        num_days = 1
        result = self.filtered_total(start, end, num_days)
        return result
        
    def next_week(self):
        today = datetime.date.today()
        last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1) 
        start = last_monday
        end = last_monday + datetime.timedelta(6)
        num_days = 1
        result = self.filtered_total(start, end, num_days)
        return result
        
    def thirty_days(self):
        first_day = datetime.date.today()
        last_day = first_day + datetime.timedelta(30)
        start = first_day
        end = last_day
        num_days = 4
        result = self.filtered_total(start, end, num_days)
        return result
        
    def sixty_days(self):
        first_day = datetime.date.today()
        last_day = first_day + datetime.timedelta(60)
        start = first_day
        end = last_day
        num_days = 8
        result = self.filtered_total(start, end, num_days)
        return result
    
    def ninety_days(self):
        first_day = datetime.date.today()
        last_day = first_day + datetime.timedelta(90)
        start = first_day
        end = last_day
        num_days = 12
        result = self.filtered_total(start, end, num_days)
        return result        
        
    # def next_month(self):
        
    # def 3_months(self):
        
    # def 6_months(self):
        
    

class Time_Off(models.Model):
    user_id = models.ForeignKey(Resource)
    date = models.DateField()
    hours_lost = models.IntegerField()

    def __str__(self):
        return '%s - %s - %s hours lost' % (self.user_id, self.date, self.hours_lost)
    
class Passwords(models.Model):
    user_id = models.ForeignKey(Resource)
    pw_string = models.CharField(max_length=150)

    def __str__(self):
        return self.user_id

#work days with boolian for active or not
class Workdays(models.Model):
    Sunday = 'Sun'
    Monday = 'Mon'
    Tuesday = 'Tue'
    Wednesday = 'Wed'
    Thursday = 'Thu'
    Friday = 'Fri'
    Saturday = 'Sat'
    day_choices = (
        (Sunday, 'Sunday'),
        (Monday, 'Monday'),
        (Tuesday, 'Tuesday'),
        (Wednesday, 'Wednesday'),
        (Thursday,'Thursday'),
        (Friday,'Friday'),
        (Saturday, 'Saturday'),
    )
    day_name = models.CharField(max_length=10, choices=day_choices, default=Monday)
    active = models.BooleanField(default=True)

    def __str__(self):
            return '%s %s' % (self.day_name, self.active)

        
class Schedule(models.Model):
    user_id = models.ForeignKey(Resource)
    day = models.ForeignKey(Workdays)
    times = ( 
        (600, '6:00AM'),
        (630, '6:30AM'),
        (700, '7:00AM'),
        (730, '7:30AM'),
        (800, '8:00AM'),
        (830, '8:30AM'),
        (900, '9:00AM'),
        (930, '9:30AM'),
        (1000, '10:00AM'),
        (1030, '10:30AM'),
        (1100, '11:00AM'),
        (1130, '11:30AM'),
        (1200, '12:00PM'),
        (1230, '12:30PM'),
        (1300, '1:00PM'),
        (1330, '1:30PM'),
        (1400, '2:00PM'),
        (1430, '2:30PM'),
        (1500, '3:00PM'),
        (1530, '3:30PM'),
        (1600, '4:00PM'),
        (1630, '4:30PM'),
        (1700, '5:00PM'),
        (1730, '5:30PM'),
        (1800, '6:00PM'),
        (1830, '6:30PM'),
    )
    start_time = models.IntegerField(choices=times, default=800)
    end_time = models.IntegerField(choices=times, default=1700)
    lunch = models.CharField(max_length=25, blank=True )

    def __str__(self):
        return '%s %s' % (self.user_id, self.day)


#For Project
class Project_Type(models.Model):
    project_type = models.CharField(max_length=150)

    def __str__(self):
        return self.project_type

class Project(models.Model):
    project_name = models.CharField(max_length=150)
    project_type = models.ForeignKey(Project_Type)
    created_date = models.DateField(default=timezone.now)
    start_date = models.DateField()
    end_date = models.DateField()
    pm_scope = models.IntegerField()
    dev_scope = models.IntegerField()
    design_scope = models.IntegerField()
    testing_scope = models.IntegerField(default=0)

    def total_scope(self):
        scope = Allocation.objects.filter(project_id = self).aggregate(Sum('allocated_hours')).values()
        return scope[0]
        
    
    def __str__(self):
        return self.project_name
        


#Resource & Project Linking table     
class Allocation(models.Model):
    active = models.BooleanField(default=True)
    user_id = models.ForeignKey(Resource)
    project_id = models.ForeignKey(Project)
    week = models.DateField(default=timezone.now)
    allocated_hours = models.IntegerField(default=0)
    actual_hours = models.IntegerField(default=0)
    
    
    def __str__(self):
        return '%s' % (self.user_id)

    def allocation_actual_overage(self):
        a = Allocation.objects.filter(project_id = self.project_id)
        total_allo = 0
        total_act = 0
        total_over = 0
        for i in a:
            if i.user_id == self.user_id:
                total_allo += i.allocated_hours
                total_act += i.actual_hours
            total_over = total_allo - total_act
        return total_allo, total_act, total_over
        
    def return_allocation(self):
        a = self.allocation_actual_overage
        return a()[0]
        
    def return_actual(self):
        a = self.allocation_actual_overage
        return a()[1]
        
    def return_overage(self):
        a = self.allocation_actual_overage
        return a()[2]       
        

    #for resource Profile

    def this_week(self):
        today = datetime.date.today()
        last_monday = today - datetime.timedelta(days=today.weekday()) 
        start = last_monday
        end = last_monday + datetime.timedelta(6)        
        allocation = Allocation.objects.filter(week__range=[start, end]).filter(user_id=self.user_id).filter(active=True).filter(project_id=self.project_id)
        a = allocation[0]                
        return a.allocated_hours        
        
    def total_left(self):
        today = datetime.date.today()
        last_monday = today - datetime.timedelta(days=today.weekday()) 
        start = last_monday
        end = self.project_id.end_date
        allocation = Allocation.objects.filter(week__range=[start, end]).filter(user_id=self.user_id).filter(active=True).filter(project_id=self.project_id).aggregate(Sum('allocated_hours')).values()
        a = allocation[0]                
        return a
        
    def first_allo_date(self):
        first = Allocation.objects.filter(user_id=self.user_id).filter(active=True).filter(project_id=self.project_id).annotate(min=Min('week'))
        date = first[0]
        return date.min
        
    def last_allo_date(self):
        last = Allocation.objects.filter(user_id=self.user_id).filter(active=True).filter(project_id=self.project_id).order_by('week').values('week')
        date = last.last()
        return date['week']
        
        
        

#For holidays - Does apply to all resources
class Holidays(models.Model):
    holiday_name = models.CharField(max_length=150)
    holiday_date = models.DateField()
    hours_lost = models.IntegerField()

    def __str__(self):
        return '%s - %s' % (self.holiday_date, self.holiday_name)
    
class settings(models.Model):
    setting_name = models.CharField(max_length=250)
    setting_int = models.IntegerField(null=True)
    setting_bool = models.NullBooleanField()
    
    def __str__(self):
        return self.setting_name
        
        
        
