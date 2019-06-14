from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from copacity.forms import edit_manager_info
from copacity.models import Resource
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def edit_manager(request, resource_id):

    
    this_manager = User.objects.get(pk=resource_id)
    data = model_to_dict(this_manager)
    form = edit_manager_info(initial=data)
    if request.method == 'POST':
        form = edit_manager_info(request.POST, instance=this_manager)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/users/')
    
    return render(request, '../templates/copacity/edit_manager.html', {
        'form': form,
        'resource_id': resource_id,
        })
