from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required
def settings_work_days(request):
    a = 'settings_work_days'

    
    
    return render(request, '../templates/copacity/settings_work_days.html', {
        'a':a,
        })