from django.shortcuts import render
from copacity.forms import edit_project_info
from django.http import HttpResponseRedirect
from copacity.models import Project
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required

@login_required
def edit_project (request, offset):
    this_project = Project.objects.get(pk=offset)
    data = model_to_dict(this_project)
    form = edit_project_info(initial=data)
    if request.method == 'POST':
        form = edit_project_info(request.POST, instance=this_project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/project_profile/%s/' % offset)

    
    a = this_project.project_name

    return render(request, '../templates/copacity/edit_project.html', {
        'form': form,
        'a': a,
        'offset': offset,
        })
