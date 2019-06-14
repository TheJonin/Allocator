from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from copacity.models import Time_Off, Resource
import datetime
from copacity.forms import time_off
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django import forms


@login_required
def edit_timeoff(request, resource_id):
    resource_name = Resource.objects.get(pk=resource_id)

    time_off_list = Time_Off.objects.filter(user_id=resource_id).filter(date__gt=datetime.date.today()-datetime.timedelta(1)).order_by('date')


#------------
#Delete Time_off Record
#------------


    class remove_time_off(forms.Form):

        active = forms.ModelMultipleChoiceField(
            queryset = time_off_list,
            widget = forms.CheckboxSelectMultiple,
            required=False,
            label=""
            )

    form_delete = remove_time_off
    if request.method == 'POST':
        form = remove_time_off(request.POST)
        if form.is_valid():
            for item in form.cleaned_data['active']:
                Time_Off.objects.filter(id = item.id).delete()
                
#------------
#Add Time_off Record
#------------
    
    user=Time_Off(user_id = Resource.objects.get(pk=resource_id))
    form = time_off()
    if request.method == 'POST':
        form = time_off(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_timeoff/%s/' % resource_id)


    
    return render(request, '../templates/copacity/edit_timeoff.html', {
        'resource_id':resource_id,
        'resource_name': resource_name,
        'time_off_list': time_off_list,
        'form': form,
        "form_delete":form_delete,
        })