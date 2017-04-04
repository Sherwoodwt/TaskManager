from django.conf.urls import url
from views import (
    tasks,
    view_task,
    create_task,
    edit_task,
    delete_task,
    accept_task,
    finish_task,
    finished_filter
)

urlpatterns = [
    url(r'^$', tasks, name="tasklist"),
    url(r'^create/$', create_task, name="createTask"),
    url(r'^(?P<task_id>[0-9]+)/$', view_task, name="viewTask"),
    url(r'^(?P<task_id>[0-9]+)/edit/$', edit_task, name="editTask"),
    url(r'^(?P<task_id>[0-9]+)/delete/$', delete_task, name="deleteTask"),
    url(r'^(?P<task_id>[0-9]+)/accept/$', accept_task, name="acceptTask"),
    url(r'^(?P<task_id>[0-9]+)/finish/$', finish_task, name="finishTask"),
    url(r'^finished_filter/$', finished_filter, name="finishedFilter"),
]
