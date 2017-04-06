from django import forms
from models import Task, Comment

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

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = (
            'text',
        )

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})
        }
