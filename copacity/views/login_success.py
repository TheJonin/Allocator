from django.http import HttpResponseRedirect
from copacity.models import Resource
from django.contrib.auth.models import User


def login_success(request):
    if request.user.is_authenticated():
        username = request.user.id
        
        
        
    """
    Redirects users based on whether they are in the admins group
    """
    if request.user.groups.filter(name="Manager").exists():
        # user is an admin
        return HttpResponseRedirect('/copacity_list/')
    else:
        resource_id = Resource.objects.get(user_id=username)
        return HttpResponseRedirect('/resource_profile/%s/' % resource_id.id)
        
        