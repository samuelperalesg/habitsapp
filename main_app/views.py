from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.core.exceptions import ValidationError
from .models import Habit
from .forms import CustomUserCreationForm, HabitForm

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

# Updating Habit's Completion
def update_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    if request.method == "POST":
        habit.is_done = 'is_done' in request.POST
        habit.save()
    return redirect('dashboard')



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

from .forms import HabitForm  # Don't forget to import HabitForm

# Create Habit

class HabitCreate(LoginRequiredMixin, CreateView):
    model = Habit
    form_class = HabitForm  # Use form_class instead of fields

    def get_success_url(self):
        return reverse('dashboard')

    # User model validation
    def form_valid(self, form):
        print("HabitCreate - Form is being submitted.")  # Debug statement
        form.instance.user = self.request.user
        if form.is_valid():
            print("HabitCreate - Form is valid.")  # Debug statement
            return super().form_valid(form)
        else:
            print(f"HabitCreate - Form errors: {form.errors}")  # Debug statement to print form errors
            return self.form_invalid(form)


# Update Habit

class HabitUpdate(LoginRequiredMixin, UserPermissionMixin, UpdateView):
    model = Habit
    form_class = HabitForm  # Use form_class instead of fields
    
    def form_valid(self, form):
        print("HabitUpdate - Form is being submitted.")  # Debug statement
        healthy = form.cleaned_data.get('healthy')
        plan_of_action = form.cleaned_data.get('plan_of_action')

        if healthy:  # if healthy is true, we bypass the plan_of_action requirement
            return super().form_valid(form)

        if not plan_of_action:  # if healthy is not true and plan_of_action is not provided
            form.add_error('plan_of_action', 'This field is required.')
            return self.form_invalid(form)

        return super().form_valid(form)

# Delete Habit

class HabitDelete(LoginRequiredMixin, UserPermissionMixin, DeleteView):
    model = Habit

    def get_success_url(self):
        return reverse('dashboard')

    def dispatch(self, request, *args, **kwargs):
        return super(HabitDelete, self).dispatch(request, *args, **kwargs)
