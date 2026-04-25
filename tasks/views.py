from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import CreateTaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "index.html")


@login_required
def tasks(request):
    tasks = Task.objects.filter(created_by=request.user, date_completed=None)
    return render(request, 'tasks.html', {'tasks': tasks})


def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {
            'form': CreateTaskForm
        })
    else:
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('tasks')
        else:
            return render(request, "create_task.html",
                          {"form": CreateTaskForm,
                           'error': 'Revisa bien los campos'})


@login_required
def task_detail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, id=task_id, created_by=request.user)
        form = CreateTaskForm(instance=task)
        return render(request, "task_detail.html", {"task": task,
                                                    "form": form})
    try:
        task = get_object_or_404(Task, id=task_id, created_by=request.user)
        form = CreateTaskForm(request.POST, instance=task)
        form.save()
        return redirect('tasks')
    except ValueError:
        return render(request, "task_detail.html", {"task": task,
                                                    "form": form,
                                                    'error': 'Error Updating'})


@login_required
def tasks_completed_list(request):
    tasks = Task.objects.filter(created_by=request.user,
                                date_completed__isnull= False) # NOQA
    print(tasks)
    return render(request, 'tasks_completed.html', {
                    'tasks': tasks})


@login_required
def task_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id, created_by=request.user)
    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, created_by=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


def create_user(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(request.POST["username"],
                                                password=request.POST["password1"])  # NOQA
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, "signup.html", {
                    "form": UserCreationForm,
                    'error': "Username Already Exist"})
        return render(request, "signup.html", {
                    "form": UserCreationForm,
                    'error': "Passwords Dont Match"})


def log_in(request):
    if request.method == "GET":
        return render(request, "login.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            username=request.POST["username"],
            password=request.POST["password"]
        )
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(
                request,
                "login.html",
                {"form": AuthenticationForm,
                 "error": "Usuario o Clave incorrecta"})


def log_out(request):
    logout(request)
    return redirect('home')
