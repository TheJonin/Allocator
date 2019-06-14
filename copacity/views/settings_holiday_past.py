from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse,HttpResponseRedirect
from copacity.models import Holidays
from copacity.forms import holidays
import datetime

from django.contrib.auth.decorators import login_required

@login_required
def settings_holiday_past(request):

    holiday_list = Holidays.objects.filter(holiday_date__lt=datetime.date.today()).order_by('holiday_date')
    
    
    
    return render(request, '../templates/copacity/settings_holiday_past.html', {
        'holiday_list':holiday_list,
        })