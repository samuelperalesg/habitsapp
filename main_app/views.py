from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.utils import timezone
from .models import Habit, Day
from .forms import CustomUserCreationForm, HabitForm
from datetime import  datetime


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
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Signup View
def user_signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    error_message = ''
    form = CustomUserCreationForm(request.POST) if request.method == 'POST' else CustomUserCreationForm()

    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
    else:
        error_message = 'Invalid signup - Please try again'

    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

# Updating Habit's Completion
def update_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    if request.method == "POST":
        is_done = 'is_done' in request.POST
        habit.is_done = is_done
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

# Calendar View
@login_required
# ... [other imports and code]
def calendar_view(request):
    events = []
    days = Day.objects.filter(user=request.user)  # Filtering by the logged-in user
    
    for day in days:
        healthy_habits = day.habits_completed.filter(healthy=True)
        
        if healthy_habits.count() == 0:  # If there are no healthy habits, no need to color the day
            continue
        
        completed_healthy_habits = healthy_habits.filter(is_done=True)
        
        if completed_healthy_habits.count() == healthy_habits.count():
            color = '#B3FFB3'  # Pastel Green
        elif completed_healthy_habits.count() > 0:
            color = '#FFFFB3'  # Pastel Yellow
        else:
            color = '#FFB3B3'  # Pastel Red
            
        events.append({
            'start': day.date.strftime('%Y-%m-%d'),  # convert to string
            'color': color,
            'display': 'background'  # makes the color fill the entire box
        })

    return render(request, 'calendar/calendar.html', {'events': events})


# Day Detail View
@login_required
def day_detail_view(request, date): 
    day_date = datetime.strptime(date, "%Y-%m-%d").date()
    day, created = Day.objects.get_or_create(date=day_date, user=request.user)
    return render(request, 'calendar/day_detail.html', {'day': day})


# Adding to calendar
@login_required
def add_to_calendar(request):
    if request.method == "POST":
        today = timezone.localtime(timezone.now()).date()
        day, created = Day.objects.get_or_create(date=today, user=request.user)
        completed_habits = Habit.objects.filter(user=request.user, is_done=True)
        day.habits_completed.set(completed_habits)
        return redirect('day_detail_view', date=day.date)  # Updated to use 'date' instead of 'day_id'
    else:
        return HttpResponseForbidden()

# Class Based Views (CBVs) ====================================================================================
# Create Habit
class HabitCreate(LoginRequiredMixin, CreateView):
    model = Habit
    form_class = HabitForm

    def get_success_url(self):
        return reverse('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.is_valid():
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

# Update Habit
class HabitUpdate(LoginRequiredMixin, UserPermissionMixin, UpdateView):
    model = Habit
    form_class = HabitForm
    
    def form_valid(self, form):
        healthy = form.cleaned_data.get('healthy')
        plan_of_action = form.cleaned_data.get('plan_of_action')

        if healthy or plan_of_action:  
            return super().form_valid(form)
        else:  
            form.add_error('plan_of_action', 'This field is required.')
            return self.form_invalid(form)

# Delete Habit
class HabitDelete(LoginRequiredMixin, UserPermissionMixin, DeleteView):
    model = Habit

    def get_success_url(self):
        return reverse('dashboard')
