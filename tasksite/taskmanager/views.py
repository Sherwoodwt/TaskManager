from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.contrib.auth.models import User

from forms import TaskForm, CommentForm
from models import Task, Comment, UserProfile

from sns_functions import *

# Create your views here.

@login_required
def create_user_profile_or_skip(request):
    '''
    If request.user has no userprofile, it is created, otherwise move on to main page.
    This ensures that all logged in users have UserProfiles.
    '''
    if not UserProfile.objects.filter(user=request.user):
        user_profile = UserProfile(user=request.user)
        user_profile.save()
    return HttpResponseRedirect(reverse('tasklist'))

@login_required
def settings(request):
    context = {
        "is_notifiable": request.user.userprofile.is_notifiable,
    }
    return render(request, 'settings.html', context)

@login_required
def tasks(request):
    tasks = Task.objects.all().order_by('-created_at')
    unfinished = request.session.get('unfinished')
    if unfinished:
        tasks = tasks.filter(finished=False)
    other_users = User.objects.all().exclude(pk=request.user.pk)
    context = {
        'tasks': tasks,
        'other_users': other_users,
        'unfinished': request.session.get('unfinished'),
    }
    return render(request, 'task_templates/list.html', context)

@login_required
def create_task(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.created_by = request.user
        instance.save()
        if instance.assignee != None and instance.created_by != instance.assignee:
            notify_assigned_task(instance)
        return HttpResponseRedirect(reverse('tasklist'))
    context = {
        'form': form,
    }
    return render(request, 'task_templates/create_edit.html', context)

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid:
            instance = form.save(commit=False)
            will_notify = False
            if instance.assignee != task.assignee:
                will_notify = True

            task.title = instance.title
            task.description = instance.description
            task.assignee = instance.assignee
            task.difficulty = instance.difficulty
            task.due_date = instance.due_date
            task.save()
            if will_notify:
                notify_assigned_task(task)
            return HttpResponseRedirect(reverse('viewTask', kwargs={'task_id': task_id}))
    else:
        fields = {
            'title': task.title,
            'description': task.description,
            'assignee': task.assignee,
            'difficulty': task.difficulty,
            'due_date': task.due_date,
        }
        form = TaskForm(initial=fields)
        context = {
            'form': form,
        }
    return render(request, 'task_templates/create_edit.html', context)

@login_required
def view_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    comments = Comment.objects.filter(task=task)
    commentform = CommentForm(request.POST or None)
    if commentform.is_valid():
        instance = commentform.save(commit=False)
        instance.created_by = request.user
        instance.task = task
        instance.save()
        commentform = CommentForm()
    context = {
        'task': task,
        'comments': comments,
        'commentform': commentform,
    }
    return render(request, 'task_templates/view.html', context)

#############
# Functions #
#############




####################
# Additional Views #
####################

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return HttpResponseRedirect(reverse('tasklist'))

@login_required
def accept_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.accept(request.user)
    return HttpResponseRedirect(reverse('viewTask', kwargs={'task_id': task_id}))

@login_required
def finish_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.finish()
    return HttpResponseRedirect(reverse('viewTask', kwargs={'task_id': task_id}))

@login_required
def finished_filter(request):
    request.session['unfinished'] = not request.session.get('unfinished')
    return HttpResponseRedirect(reverse('tasklist'))

@login_required
def switch_notifications(request):
    profile = request.user.userprofile
    profile.is_notifiable = not profile.is_notifiable
    if profile.is_notifiable and profile.notification_arn is None:
        profile.notification_arn = create_topic(request.user)
        profile.subscription_arn = create_subscription(profile.notification_arn, request.user)
    profile.save()
    return HttpResponseRedirect(reverse('settings'))
