from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from copacity.models import Resource
from copacity.forms import schedule_edit
from django.forms.models import model_to_dict
from copacity.models import Schedule
from django.contrib.auth.decorators import login_required

@login_required
def edit_schedule(request, resource_id):
    resource_name = Resource.objects.get(pk=resource_id)

    Schedule_record_list = Schedule.objects.filter(user_id = resource_id).order_by('day')

    form_list = []
    for s in Schedule_record_list:
        # form_list.append(s.day.day_name)
        form = schedule_edit(instance = s, prefix = s.pk)
        form_list.append((s.day.day_name, form))
        if request.method == 'POST':
            form = schedule_edit(request.POST, instance = s, prefix = s.pk)
            if form.is_valid():
                form.save()
    
    if request.method == 'POST':
        return HttpResponseRedirect('/resource_profile/%s/' % resource_id)


    
    return render(request, '../templates/copacity/edit_schedule.html', {
        'resource_name': resource_name,
        'form_list': form_list,
        'resource_id': resource_id
        })