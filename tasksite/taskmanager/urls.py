from django.conf.urls import url
from views import (
    tasks,
    view_task,
    create_task,
    edit_task,
    delete_task,
)

urlpatterns = [
    url(r'^$', tasks, name="tasklist"),
    url(r'^create/$', create_task, name="createTask"),
    url(r'^([0-9]+)/$', view_task, name="viewTask"),
    url(r'^([0-9]+)/edit/$', edit_task, name="editTask"),
    url(r'^([0-9]+)/delete/$', delete_task, name="deleteTask"),
]
