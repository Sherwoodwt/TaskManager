from __future__ import unicode_literals
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

from django.db import models

# Create your models here.

class DateModel(models.Model):
    '''Abstract model to include created_at and updated_at'''
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        '''Create or Update date set to current time on save'''
        if not self.id:
            self.created_at = timezone.localtime(timezone.now())
        self.updated_at = timezone.localtime(timezone.now())
        super(DateModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class Task(DateModel):
    assignee = models.ForeignKey(User, null=True, blank=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    created_by = models.CharField(max_length=100)
    difficulty = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5),])
    due_date = models.DateTimeField()
    finished = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title
    
class Comment(DateModel):
    task = models.ForeignKey(Task)
    created_by = models.ForeignKey(User)
    text = models.TextField()

    def __unicode__(self):
        return self.text
