from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from copacity.forms import new_resource_form
from copacity.models import Project, User_Type, Schedule, Resource, Workdays
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

@login_required
def new_resource(request):
    
    form = new_resource_form()
    if request.method == 'POST':
        user_type = Resource(user_type = User_Type.objects.get(user_type = 'Resource'))
        form = new_resource_form(request.POST, instance = user_type)
        if form.is_valid():
            form.save(commit=False)
            resource_name = form.cleaned_data['resource_name']
            email_address = form.cleaned_data ['email_address']
            weekly_copacity = form.cleaned_data['weekly_copacity']
            username = form.cleaned_data['username'].lower()
            #---------
            #Need to set password manualy later
            #---------
            password = 'Changeme123'
            new_user = User.objects.create_user(username, email_address, password)
            new_user.save()
            g = Group.objects.get(name='Resource')
            g.user_set.add(new_user)
            form.cleaned_data['user'] = new_user.pk
            form.save()
            #------
            #setting Resource User Foreign Key to User id
            #--------
            
            u_id = User.objects.get(username = username)
            r_record = Resource.objects.get(resource_name = resource_name)
            r_record.user = u_id
            r_record.save()
            
            #------
            # create schedule records
            #--------
            resource = Resource.objects.get(resource_name = resource_name)
            
            mon = Schedule(user_id = resource, day = Workdays.objects.get(day_name = 'Mon'), lunch = '1hr Lunch')
            mon.save()
            tue = Schedule(user_id = resource, day = Workdays.objects.get(day_name = 'Tue'), lunch = '1hr Lunch')
            tue.save()
            wed = Schedule(user_id = resource, day = Workdays.objects.get(day_name = 'Wed'), lunch = '1hr Lunch')
            wed.save()
            thu = Schedule(user_id = resource, day = Workdays.objects.get(day_name = 'Thu'), lunch = '1hr Lunch')
            thu.save()
            fri = Schedule(user_id = resource, day = Workdays.objects.get(day_name = 'Fri'), lunch = '1hr Lunch')
            fri.save()

            return HttpResponseRedirect('/copacity_list/')

    return render(request, '../templates/copacity/new_resource.html', {
        'form': form,
        })


