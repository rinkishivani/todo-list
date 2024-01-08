from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.contrib.auth.models import User


class Worker(models.Model):
    name = models.CharField(max_length=50)


class ToDoList(models.Model):
    title = models.CharField(max_length=100)
    details = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    PROGRESS_CHOICES = (
        ('pending', 'pending'),
        ('in progress..', 'in progress'),
        ('completed', 'completed'),
    )
    progress = models.CharField(max_length=30, choices=PROGRESS_CHOICES, default='pending')
    workers = models.ManyToManyField(Worker, through='TodoWorkerThrough')
    document = models.FileField(upload_to='documents/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-date']


class TodoWorkerThrough(models.Model):
    todo = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    days = models.CharField(max_length=10)
# class Hobbies(Model):


class Product(models.Model):
    name = models.CharField(max_length=50)
    workers = models.ManyToManyField(Worker, through='ProductWorkersThrough')


class ProductWorkersThrough(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    in_time = models.DateTimeField(null=True, blank=True)



class Machine(models.Model):
    name = models.CharField(max_length=50)
    workers = models.ManyToManyField(Worker)