from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from copacity.models import Time_Off, Resource
import datetime
from django.contrib.auth.decorators import login_required

@login_required
def edit_timeoff_past(request, resource_id):
    resource_name = Resource.objects.get(pk=resource_id)

    time_off_list = Time_Off.objects.filter(user_id=resource_id).filter(date__lt=datetime.date.today()).order_by('date')



    
    return render(request, '../templates/copacity/edit_timeoff_past.html', {
        'resource_id':resource_id,
        'resource_name': resource_name,
        'time_off_list': time_off_list,

        })