from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from copacity.models import Resource
from copacity.tables import copacity_table
from django.contrib.auth.decorators import login_required

@login_required
def copacity_list(request):
    a = "copacity_list"
    table = copacity_table(Resource.objects.filter(active=True).order_by("resource_name"))
    
    return render(request, '../templates/copacity/copacity_list.html', {
        'a': a,
        'table': table,
        })
