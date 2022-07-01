from tkinter import CASCADE
from tkinter.tix import Tree
from typing import OrderedDict
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# one to many relations
class Books(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    review = models.IntegerField()
    finished_reading = models.BooleanField(default=False)
    started_reading_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['finished_reading']
