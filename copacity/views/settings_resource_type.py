from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse,HttpResponseRedirect
from copacity.models import Resource_Type
from copacity.forms import resource_type
from django.contrib.auth.decorators import login_required

@login_required
def settings_resource_type(request):

    resource_type_list = Resource_Type.objects.all()
    
    form = resource_type()
    if request.method == 'POST':
        form = resource_type(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/settings_resource_type/')

    
    
    return render(request, '../templates/copacity/settings_resource_type.html', {
        'resource_type_list':resource_type_list,
        'form': form,
        })