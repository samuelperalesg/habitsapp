from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from .models import Habit
from .forms import CustomUserCreationForm

# Custom Mixin for User Permission Check


class UserPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

# Views
# ========================================================

# Welcome/Login View

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = AuthenticationForm()  # Include an instance of the form
    return render(request, 'registration/login.html', {'form': form})  # Pass the form as context data


# Signup View

def user_signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    error_message = ''
    form = CustomUserCreationForm(request.POST) if request.method == 'POST' else CustomUserCreationForm()

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = 'Please try again'

    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


# Dashboard - Habits View

@login_required
def dashboard(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'habits': habits})


# Dashboard - Habits Detail View

@login_required
def habits_detail(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    return render(request, 'habits/detail.html', {'habit': habit})


# Inspo View

@login_required
def inspo(request):
    return render(request, 'inspo.html')


# Class Based Views (CBVs) =====================


# Create Habit

class HabitCreate(LoginRequiredMixin, CreateView):
    model = Habit
    fields = ['habit_name', 'healthy', 'plan_of_action', 'external_cue', 'internal_cue']

    def get_success_url(self):
        return reverse('dashboard')

    # User model validation
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Update Habit

class HabitUpdate(LoginRequiredMixin, UserPermissionMixin, UpdateView):
    model = Habit
    fields = ['habit_name', 'healthy', 'plan_of_action', 'external_cue', 'internal_cue']

    def dispatch(self, request, *args, **kwargs):
        return super(HabitUpdate, self).dispatch(request, *args, **kwargs)


# Delete Habit

class HabitDelete(LoginRequiredMixin, UserPermissionMixin, DeleteView):
    model = Habit

    def get_success_url(self):
        return reverse('dashboard')

    def dispatch(self, request, *args, **kwargs):
        return super(HabitDelete, self).dispatch(request, *args, **kwargs)
