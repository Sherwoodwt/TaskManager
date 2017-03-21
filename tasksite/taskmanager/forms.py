from django import forms
from models import Task

from django.forms.extras.widgets import SelectDateWidget

class TaskForm(forms.ModelForm):


    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'assignee',
            'difficulty',
            'due_date',
        )

        widgets = {
            'due_date': SelectDateWidget(),
        }
