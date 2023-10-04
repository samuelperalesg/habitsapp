from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
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
def calendar_view(request):
    events = []
    days = Day.objects.filter(user=request.user)
    
    for day in days:
        if not day.color_status:  # Ensure color is set
            continue
        
        event = {
            'start': day.date.strftime('%Y-%m-%d'),
            'color': day.color_status,
            'display': 'background'
        }
        
        # Log event data
        print(f'Event for {event["start"]}: {event}')

        events.append(event)

    return render(request, 'calendar/calendar.html', {'events': events})



# Day Detail View
@login_required
def day_detail_view(request, date): 
    day_date = datetime.strptime(date, "%Y-%m-%d").date()
    day, created = Day.objects.get_or_create(date=day_date, user=request.user)

    # Log day object and creation status
    print(f"Day Created: {created}, Day Object: {day}")

    if day.habits_completed.count() == 0:
        messages.info(request, "No habits recorded for this day.")
        
    return render(request, 'calendar/day_detail.html', {'day': day})


# Adding to calendar
@login_required
def add_to_calendar(request):
    if request.method == "POST":
        today = timezone.localtime(timezone.now()).date()

        # Log today's date
        print(f'Today’s Date: {today}')

        if today > timezone.localtime(timezone.now()).date():
            messages.error(request, "Cannot add habits to future dates.")
            return redirect('calendar_view')

        day, created = Day.objects.get_or_create(date=today, user=request.user)

        # Log day object and creation status
        print(f'Day Created: {created}, Day Object: {day}')

        completed_habits = Habit.objects.filter(user=request.user, is_done=True)
        day.habits_completed.set(completed_habits)

        healthy_habits = Habit.objects.filter(user=request.user, healthy=True)
        completed_healthy_habits = healthy_habits.filter(is_done=True)

        # Check and assign a color based on completed healthy habits
        if completed_healthy_habits.count() == healthy_habits.count() and completed_healthy_habits.count() > 0:
            day.color_status = '#B3FFB3'  # Green
        elif completed_healthy_habits.count() > 0:
            day.color_status = '#FFFFB3'  # Yellow
        elif healthy_habits.exists():  # There are healthy habits but none are completed
            day.color_status = '#FFB3B3'  # Red
        else:
            # If there are no healthy habits, assign no color
            day.color_status = None

        # Log calculated color
        print(f'Calculated color: {day.color_status}')

        day.save()

        # Log stored color after save
        retrieved_day = Day.objects.get(date=today, user=request.user)
        print(f'Stored color: {retrieved_day.color_status}')

        return redirect('day_detail_view', date=day.date)
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
