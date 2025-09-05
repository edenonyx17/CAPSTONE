from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.views import (
  LoginView,
  PasswordResetView,
  PasswordResetDoneView,
  PasswordResetConfirmView,
  PasswordResetCompleteView,
)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Task
from .forms import TaskForm, RegisterForm, EditProfileForm
from datetime import date
from django.urls import reverse_lazy


# Create your views here.
# Function based views

#h home view
def home(request):
  if request.user.is_authenticated:
    return redirect('task_list')
  return render(request, 'capstone_app/home.html')

#R Register view
def register(request):
  if request.method == 'POST':
    form = RegisterForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      messages.success(request, f"Hi {request.user.username}! You have successful")
      return redirect('task_list')
    else:
      messages.error(request, 'Failed! Something went wrong')
  else:
    form = RegisterForm()
  return render(request, 'capstone_app/registration/register.html', {'form': form})

#V View to see tasks
@login_required
def task_list(request):
  queryset = Task.objects.filter(user=request.user)

  # Filtering
  status = request.GET.get('status')
  priority = request.GET.get('priority')
  category = request.GET.get('category')
  overdue = request.GET.get('overdue')

  if status:
    queryset = queryset.filter(status=status)
  if priority:
    queryset = queryset.filter(priority=priority)
  if category:
    queryset = queryset.filter(category=category)
  if overdue == 'yes':
    queryset = queryset.filter(Q(due_date__lt=date.today()) & Q(status='pending'))

  # sorting the newest at the top
  sort = request.GET.get('sort', '-date_created')
  queryset = queryset.order_by(sort)

  # Show limited tasks
  paginator = Paginator(queryset, 5)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  context = {
    'page_obj': page_obj,
    'status': status,
    'priority': priority,
    'category': category,
    'overdue': overdue,
    'sort': sort,
  }
  return render(request, 'capstone_app/task_list.html', context)

# Creating task view
@login_required
def task_create(request):
  if request.method == 'POST':
    form = TaskForm(request.POST)
    if form.is_valid():
      task = form.save(commit=False)
      task.user = request.user
      task.save()
      messages.success(request, f'Hi {request.user.username}! Task created successfully')
      return redirect('task_list')
    else:
      messages.error(request, f'Hi {request.user.username}! There was an error creating the task. Please check the form')
  else:
    form = TaskForm()
  return render(request, 'capstone_app/task_form.html', {'form': form, 'action': 'Create'})

# Updating task view
@login_required
def task_update(request, pk):
  task = get_object_or_404(Task, pk=pk, user=request.user)
  if request.method == 'POST':
    form = TaskForm(request.POST, instance=task)
    if form.is_valid():
      form.save()
      messages.success(request, f'Hi {request.user.username}! Task updated successfully')
      return redirect('task_list')
    else:
      messages.error(request, f'Hi {request.user.username}! There was an error updating the task. Please check the form')
  else:
    form = TaskForm(instance=task)
  return render(request, 'capstone_app/task_form.html', {'form': form, 'action': 'Update'})

# Task detail
@login_required
def task_detail(request, pk):
  task = get_object_or_404(Task, pk=pk, user=request.user)
  return render(request, 'capstone_app/task_detail.html', {'task': task})


# Deleting task view
@login_required
def task_delete(request, pk):
  task = get_object_or_404(Task, pk=pk, user=request.user)
  if request.method == 'POST':
    task.delete()
    messages.success(request, f'Hi {request.user.username}! Task deleted successfully')
    return redirect('task_list')
  return render(request, 'capstone_app/confirm_delete.html', {'task': task})

# Toggle task status view
@login_required
def task_toggle_status(request, pk):
  task = get_object_or_404(Task, pk=pk, user=request.user)
  task.status = 'completed' if task.status == 'pending' else 'pending'
  task.save()
  if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    return JsonResponse({'status': task.status})
  messages.success(request, f'Hi {request.user.username}! Task status updated successfully')
  return redirect('task_list')

# Login view
# """class CustomLoginView(LoginView):
#   template_name = 'capstone_app/registration/login.html'
#   redirect_authenticated_user = True

#   def get_success_url(self):
#     return reverse_lazy('task_list')
# """


# Password reset views
class PasswordResetView(PasswordResetView):
  template_name = 'capstone_app/registration/password_reset.html'
  success_url = reverse_lazy('password_reset_done')

class PasswordResetDoneView(PasswordResetDoneView):
  template_name = 'capstone_app/registration/password_reset_done.html'

class PasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'capstone_app/registration/password_reset_confirm.html'
  success_url = reverse_lazy('password_reset_complete')

class PasswordResetCompleteView(PasswordResetCompleteView):
  template_name = 'capstone_app/registration/password_reset_complete.html'

# Profile view
@login_required
def profile(request):
  return render(request, 'capstone_app/profile.html', {'user': request.user})

# Edit profile view
@login_required
def edit_profile(request):
  if request.method == 'POST':
    form = EditProfileForm(request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      messages.success(request, f'Hi {request.user.username}! Profile updated successfully')
      return redirect('profile')
    else:
      messages.error(request, f'Hi {request.user.username}! There was an error updating the profile. Please check the form')
  else:
    form = EditProfileForm(instance=request.user)
  return render(request, 'capstone_app/profile_edit.html', {'form': form})

# Reminder view
@login_required
def reminder(request):
  # """today = date.today()
  # task = Task.objects.filter(user=request.user, status='pending', due_date__isnull=False).order_by('due_date')
  # context = {
  #   'task': task,
  #   'today': today,
  # }
  # return render(request, 'capstone_app/reminder.html', context)"""
  queryset = Task.objects.filter(user=request.user, due_date__lt=date.today(), status='pending')
  return render(request, 'capstone_app/reminder.html', {'queryset': queryset})


# Password change views
@login_required
def change_password(request):
  if request.method == 'POST':
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
      user = form.save()
      update_session_auth_hash(request, user)
      messages.success(request, f'Hi {request.user.username}! Your password was successfully updated!')
      return redirect('profile')
    else:
      messages.error(request, f'Hi {request.user.username}! There was an error updating your password. Please check the form andPlease correct the error below.')
  else:
    form = PasswordChangeForm(request.user)
  return render(request, 'capstone_app/registration/password_change.html', {'form': form})


@login_required
def change_password_done(request):
  return render(request, 'capstone_app/registration/password_change_done.html')