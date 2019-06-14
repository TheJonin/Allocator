from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from copacity.models import Project_Type
from copacity.forms import project_type
from django.contrib.auth.decorators import login_required

@login_required
def settings_project_type(request):
    
    project_type_list = Project_Type.objects.all()
    
    form = project_type()
    if request.method == 'POST':
        form = project_type(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/settings_project_type/')

    
    
    return render(request, '../templates/copacity/settings_project_type.html', {
        'project_type_list':project_type_list,
        'form': form,
        })
        
