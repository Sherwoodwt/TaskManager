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
            created_at = timezone.now()
        updated_at = timezone.now()
        return super(Task, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class Task(DateModel):
    user = models.ForeignKeyField(User, null=True)
    name = models.CharField(max_length=150)
    description = models.TextField()
    created_by = models.ForeignKeyField(User)
    difficulty = models.PositiveIntegerField(default=0, validators=[MaxValueValidator[5],])
    due_date = models.DateTimeField()
    finished = models.BooleanField(default=False)
    
class Comment(DateModel):
    task = models.ForeignKeyField(Task)
    created_by = models.ForeignKeyField(User)
    text = models.TextField()
