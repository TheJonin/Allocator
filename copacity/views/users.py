from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from copacity.tables import managers_table


@login_required
def users(request):

    # user_lst = User.objects.filter(groups__name='Manager')
    table = managers_table(User.objects.filter(groups__name='Manager').filter(is_active=True))

    
    return render(request, '../templates/copacity/users.html', {
        "table": table,
        })
