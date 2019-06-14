from django.shortcuts import render
from django.http import HttpResponseRedirect
from copacity.models import Allocation, Resource, Project
from copacity.forms import remove_resource, add_resource
from django.db.models import Q
from django import forms
from django.contrib.auth.decorators import login_required

@login_required
def edit_project_resource (request, offset):
    list_resources = Allocation.objects.filter(project_id=offset).filter(active=True).order_by('user_id').distinct('user_id')
    # list_resource_add = Allocation.objects.filter(project_id=offset).filter(active=False).order_by('user_id').distinct('user_id')




#-------------------------
# Delete Resource
#-------------------------
    # display = {}
    # for r in list_resources:
    #     check = remove_resource(prefix = r.pk)
    #     display[r.user_id] = (check, r.user_id)
    #     user = r.user_id
    # if request.method == 'POST':
    #     for i,v in display:
    #         check = remove_resource(request.POST, prefix = r.pk)
    #         if check.is_valid():
    #             if request.POST.get("%s-%s" % (r.pk, 'active')):
    #                 Allocation.objects.filter(project_id = offset).filter(user_id = user).update(active = False)
                
    #                 return HttpResponseRedirect('/project_profile/%s/' % offset)


#-------------------------
# Delete Resource Test
#-------------------------

    class remove_resource_test(forms.Form):

        active = forms.ModelMultipleChoiceField(
            queryset = list_resources,
            widget = forms.CheckboxSelectMultiple,
            required=False,
            label=""
            )

    form = remove_resource_test
    if request.method == 'POST':
        form = remove_resource_test(request.POST)
        if form.is_valid():
            for item in form.cleaned_data['active']:
                Allocation.objects.filter(project_id = offset).filter(user_id = item.user_id).update(active = False)
                
    


#-------------------------
# Add Resource Test
#-------------------------

    queryset = Allocation.objects.filter(project_id = offset).filter(active=True).values_list('user_id__resource_name', flat=True).distinct('user_id')
    lst_avalible_resources = Resource.objects.filter(active=True).exclude(resource_name__in = queryset).distinct('resource_name')


    project = Project.objects.filter(pk=offset)
    proj_start = project.values('start_date')
    proj_end = project.values('end_date')
    
    

    class add_resource_test(forms.Form):

        non_active = forms.ModelMultipleChoiceField(
            queryset = lst_avalible_resources,
            widget = forms.CheckboxSelectMultiple,
            required=False,
            label=""
            )

    addform = add_resource_test
    if request.method == 'POST':
        addform = add_resource_test(request.POST)
        if addform.is_valid():
            for item in addform.cleaned_data['non_active']:
                if Allocation.objects.filter(project_id = offset).filter(user_id__resource_name = item.resource_name).filter(week__gt=proj_start, week__lt=proj_end).exists():
                    Allocation.objects.filter(project_id = offset).filter(user_id__resource_name = item.resource_name).update(active = True)
                else:
                    record = Allocation(
                        user_id = Resource.objects.get(pk=item.pk),
                        project_id = Project.objects.get(pk=offset),
                        week = Project.objects.get(pk=offset).start_date,
                        )
                    record.save()
                    
            return HttpResponseRedirect('/project_profile/%s/' % offset)
                    
              



# #-------------------------
# # Add Resource
# #-------------------------


    # add = {}
    # for r in lst_avalible_resources:
    #     check = add_resource(prefix = r.pk)
    #     add[r.resource_name] = (check, r.resource_name)
    #     user = r.resource_name
    #     if request.method == 'POST':
    #         check = add_resource(request.POST, prefix = r.pk)
    #         if check.is_valid():
    #             if request.POST.get("%s-%s" % (r.pk, 'active')):
    #                 if Allocation.objects.filter(project_id = offset).filter(user_id__resource_name = user).filter(week__gt=proj_start, week__lt=proj_end).exists():
    #                     Allocation.objects.filter(project_id = offset).filter(user_id__resource_name = user).update(active = True)
    #                 else:
    #                     record = Allocation(
    #                         user_id = Resource.objects.get(pk=r.id),
    #                         project_id = Project.objects.get(pk=offset),
    #                         week = Project.objects.get(pk=offset).start_date,
    #                         )
    #                     record.save()
                        
    #                 return HttpResponseRedirect('/project_profile/%s/' % offset)

                        
                        
    project_name = Project.objects.get(pk=offset)

    return render(request, '../templates/copacity/edit_project_resource.html', {
        # 'display': display,
        # 'add': add,
        'project_name':project_name,
        'offset': offset,
        'form':form,
        'addform':addform,
        # 'display_add_function': display_add_function,
        # 'display_add_function_form':display_add_function_form
        })
