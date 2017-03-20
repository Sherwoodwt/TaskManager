from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

# Create your views here.

@login_required
def tasks(request):
    return HttpResponse('killme')

@login_required
def create_task(request):
    return HttpResponse('Create Task Page')

@login_required
def edit_task(request, task_id):
    return HttpResponse('edit task page')

@login_required
def view_task(request, task_id):
    return HttpResponse('view task')
