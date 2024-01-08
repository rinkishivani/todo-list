import logging

from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from .models import ToDoList
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ToDoListForm
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.storage import default_storage
from allauth.account.forms import AddEmailForm
from allauth.account.decorators import verified_email_required

def login_page(request):
    redirect('/ToDoList/login/')
    request._messages = default_storage(request)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/ToDoList/login')
        else:
            login(request, user)
            home(request)
            return redirect('/ToDoList/home')

    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('uname')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, 'Cannot create user! username already exists.')
            return redirect('/ToDoList/register/')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )

        user.set_password(password)
        user.save()
        messages.info(request, 'user created')
        return redirect('/ToDoList/register/')

    return render(request, 'register.html')


def logout_page(request):
    logout(request)
    return render(request, 'login.html')


# Decorator for checking superuser
def superuser_decorator(original_function):
    def superuser_view(request, username=None, pk=None):
        if request.user.is_superuser:
            tasks = ToDoList.objects.filter(deleted=False)
            users = User.objects.all()
            page = request.GET.get('page', 1)
            task_paginator = Paginator(tasks, 3)
            try:
                page_no = task_paginator.page(page)
            except PageNotAnInteger:
                page_no = task_paginator.page(1)
            except EmptyPage:
                page_no = task_paginator.page(task_paginator.num_pages)
            return render(request, 'home.html', {'tasks': tasks, 'users': users, 'page_no': page_no,
                                                 'username': username, 'pk': pk})
        return render(request, 'home.html')

    return superuser_view


@login_required(login_url="/ToDoList/login")
@verified_email_required
@superuser_decorator
def home(request):
    tasks_list = ToDoList.objects.filter(deleted=False, created_by=request.user)
    user_id = request.session.get('user_id', None)
    if tasks_list:
        last_task = tasks_list[0]
    else:
        last_task = ""
    page = request.GET.get('page', 1)
    task_paginator = Paginator(tasks_list, 3)
    try:
        page_no = task_paginator.page(page)
    except PageNotAnInteger:
        page_no = task_paginator.page(1)
    except EmptyPage:
        page_no = task_paginator.page(task_paginator.num_pages)

    return render(request, 'home.html', {'tasks': tasks_list, 'last_task': last_task,
                                         'page_no': page_no, 'user_id': user_id})


@login_required(login_url="/ToDoList/login")
def superuser_home(request, username, pk):
    tasks_list = ToDoList.objects.filter(deleted=False, created_by=pk)
    users = User.objects.all()
    username = username.title()
    last_task = ''
    if tasks_list:
        last_task = tasks_list[0]
    page = request.GET.get('page', 1)
    task_paginator = Paginator(tasks_list, 3)
    try:
        page_no = task_paginator.page(page)
    except PageNotAnInteger:
        page_no = task_paginator.page(1)
    except EmptyPage:
        page_no = task_paginator.page(task_paginator.num_pages)
    return render(request, 'home.html',
                  {'tasks': tasks_list, 'last_task': last_task, 'page_no': page_no,
                   'username': username, 'users': users})


@login_required(login_url="/ToDoList/login")
def delete(request, pk):
    task = get_object_or_404(ToDoList, id=pk)
    task.delete()
    return redirect('/ToDoList/trash')


@login_required(login_url="/ToDoList/login")
def create(request):
    if request.method == "POST":
        form = ToDoListForm(request.POST, request.FILES, )
        if form.is_valid():
            todo_instance = form.save(commit=False)
            todo_instance.created_by = request.user
            todo_instance.save()
            return redirect('home')
    else:
        form = ToDoListForm()
    return render(request, 'create_task.html', {'form': form})


@login_required(login_url="/ToDoList/login")
def update(request, pk):
    tasks = get_object_or_404(ToDoList, id=pk)
    form = ToDoListForm()
    if request.method == "POST":
        updated_title = request.POST.get('title')
        updated_details = request.POST.get('details')
        if form.is_valid:
            tasks.title = updated_title
            tasks.details = updated_details
            tasks.save()
            return redirect('/ToDoList/home')
    else:
        form = ToDoListForm(initial={
            'title': tasks.title,
            'details': tasks.details,
        })
    return render(request, 'update_task.html', {'task': tasks, 'form': form})


@login_required(login_url="/ToDoList/login")
def soft_delete(request, pk):
    task = get_object_or_404(ToDoList, id=pk)
    if request.method == "POST":
        task.deleted = True
        task.save()
        messages.error(request, "Moved to trash")
        return redirect('/ToDoList/home')

    return render(request, 'confirm_delete.html', {'task': task})


@login_required(login_url="/ToDoList/login")
def trash(request):
    tasks = ToDoList.objects.filter(deleted=True, created_by=request.user)
    return render(request, 'trash.html', {'tasks': tasks})


@login_required(login_url="/ToDoList/login")
def restore(request, pk):
    task = get_object_or_404(ToDoList, id=pk)
    users = User.objects.all()
    task.deleted = False
    task.save()
    messages.success(request, "Restored")
    return redirect('/ToDoList/home', {'users': users})


@login_required(login_url="/ToDoList/login")
def task(request, pk):
    tasks = ToDoList.objects.get(id=pk)
    users = User.objects.all()
    return render(request, 'task.html', {'task': tasks, 'users': users})


# def orm(reqstr(tasks.query), User.objects.exclude(id__lt=5)]
    #     q2 = User.object.filter(Q(first_name__startswith='R'))|User.objects.filter(last_name__startswith='D'))
    # q3 =User.objects.exclude(id__lt=5)
    # for q in query:
    #
    # return HttpResponse('orm_practice.html')

# def display_request_meta(request):
#     # Access various meta information from the request
#     user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown User Agent')
#     remote_address = request.META.get('REMOTE_ADDR', 'Unknown Remote Address')
#
#     # Build a response with the meta information
#     response_content = f"User Agent: {user_agent}\nRemote Address: {remote_address}"
#     return HttpResponse(response_content, content_type="text/plain")
