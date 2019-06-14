from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required
def settings(request):
    

    return HttpResponseRedirect('/settings_project_type/')

