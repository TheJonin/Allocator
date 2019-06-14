from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from copacity.forms import new_project_form
from copacity.models import Project
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required

@login_required
def new_project(request):

    form = new_project_form()
    if request.method == 'POST':
        form = new_project_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/project_list/')



    return render(request, '../templates/copacity/new_project.html', {
        'form': form,
        })
