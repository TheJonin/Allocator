from django.shortcuts import render
from django.http import HttpResponse
from copacity.models import Project
from copacity.tables import Project_table
from django.contrib.auth.decorators import login_required
from datetime import date

@login_required
def project_list(request):
    today = date.today()
    
    table = Project_table(Project.objects.filter(end_date__gte=today).order_by("project_name"))
    table.paginate(page=request.GET.get('page', 1), per_page=50)
    
    return render(request, '../templates/copacity/project_list.html', {
        'table': table,
    })


