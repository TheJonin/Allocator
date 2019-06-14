from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse,HttpResponseRedirect
from copacity.models import Holidays
from copacity.forms import holidays, holidays_delete
import datetime
from django.contrib.auth.decorators import login_required

@login_required
def settings_holiday(request):

    holiday_list = Holidays.objects.filter(holiday_date__gt=datetime.date.today()-datetime.timedelta(1)).order_by('holiday_date')
    
    form_delete = holidays_delete
    if request.method == 'POST':
        form = holidays_delete(request.POST)
        if form.is_valid():
            for item in form.cleaned_data['active']:
                Holidays.objects.get(id = item.id ).delete()
                return HttpResponseRedirect('/settings_holiday/')
    
    form = holidays()
    if request.method == 'POST':
        form = holidays(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/settings_holiday/')
    
    
    return render(request, '../templates/copacity/settings_holiday.html', {
        'form_delete':form_delete,
        'holiday_list':holiday_list,
        'form': form,
        })