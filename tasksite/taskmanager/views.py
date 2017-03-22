from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseRedirect

from forms import TaskForm
from models import Task

# Create your views here.

@login_required
def tasks(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks
    }
    return render(request, 'task_templates/list.html', context)

@login_required
def create_task(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.created_by = request.user.username
        instance.save()
        return HttpResponseRedirect(reverse('tasklist'))
    context = {
        'form': form,
    }
    return render(request, 'task_templates/create_edit.html', context)

@login_required
def edit_task(request, task_id):
    return render(request, 'task_templates/create_edit.html')

@login_required
def view_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    context = {
        'task': task,
    }
    return render(request, 'task_templates/view.html', context)

@login_required
def delete_task(request, task_id):
    return HttpResponseRedirect(reverse('tasklist'))
