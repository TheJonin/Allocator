from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from copacity.forms import new_manager_form
from copacity.models import Project, User_Type, Schedule, Resource, Workdays
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

@login_required
def new_manager(request):
    
    form = new_manager_form()
    if request.method == 'POST':
        group = User(
            password = 'Changeme123')
        form = new_manager_form(request.POST, instance=group)
        if form.is_valid():
            form.save(commit=False)
            username = form.cleaned_data['username']
            email = form.cleaned_data ['email']
            password = 'Changeme123'
            new_manager = User.objects.create_user(username, email, password)
            new_manager.save()
            g = Group.objects.get(name='Manager')
            g.user_set.add(new_manager)
            return HttpResponseRedirect('/users/')

    return render(request, '../templates/copacity/new_manager.html', {
        'form': form,
        })




