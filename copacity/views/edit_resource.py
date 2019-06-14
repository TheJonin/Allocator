from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from copacity.forms import edit_resource_info
from copacity.models import Resource
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required

@login_required
def edit_resource(request, resource_id):

    
    this_resource = Resource.objects.get(pk=resource_id)
    data = model_to_dict(this_resource)
    form = edit_resource_info(initial=data)
    if request.method == 'POST':
        form = edit_resource_info(request.POST, instance=this_resource)
        if form.is_valid():
            form.save(commit=False)
            Resource_obj = Resource.objects.get(id=resource_id)
            resource_username = Resource_obj.user
            if form.cleaned_data['active'] == False:
                User.objects.filter(username=resource_username).update(is_active=False)
            else:
                User.objects.filter(username=resource_username).update(is_active=True)
            form.save()
            return HttpResponseRedirect('/resource_profile/%s/' % resource_id)
    
    return render(request, '../templates/copacity/edit_resource.html', {
        'form': form,
        'resource_id': resource_id,
        })
