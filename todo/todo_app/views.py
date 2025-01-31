from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # ✅ Import User model
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import json

from .models import Task
from .forms import TaskForm, RegisterForm


def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        # Create the user and hash password properly
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')  # ✅ Redirect to login after registration

    return render(request, 'todo_app/register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('task_list')  # ✅ Redirect to task list
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'todo_app/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def task_list(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        # Create the task and associate it with the logged-in user
        Task.objects.create(
            name=name,
            description=description,
            user=request.user  # ✅ Assign the logged-in user
        )

        return redirect("task_list")

    tasks = Task.objects.filter(user=request.user)
    return render(request, "todo_app/task_list.html", {"tasks": tasks})


@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)  # ✅ Ensure user owns the task
    task.delete()
    return redirect('task_list')


@login_required
@csrf_protect
def toggle_task(request, task_id):
    if request.method == "POST":
        task = Task.objects.get(id=task_id, user=request.user)  # ✅ Ensure user owns the task
        data = json.loads(request.body)
        task.completed = data.get('completed', False)
        task.save()
        return JsonResponse({"status": "success"})
