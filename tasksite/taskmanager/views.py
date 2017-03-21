from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseRedirect

from forms import TaskForm

# Create your views here.

@login_required
def tasks(request):
    return render(request, 'task_templates/list.html')

@login_required
def create_task(request):
    form = TaskForm
    context = {
        'form': form,
    }
    return render(request, 'task_templates/create_edit.html', context)

@login_required
def edit_task(request, task_id):
    return render(request, 'task_templates/create_edit.html')

@login_required
def view_task(request, task_id):
    return render(request, 'task_templates/view.html')

@login_required
def delete_task(request, task_id):
    return HttpResponseRedirect(reverse('tasklist'))
