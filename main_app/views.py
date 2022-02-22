from dataclasses import fields
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Habit

# Views
# ========================================================

# Welcome View
def welcome(request):
	return render(request, 'welcome.html')

# Signup View
def signup(request):
	return render(request, 'signup.html')

# Dashboard - Habits View
def dashboard(request):
	habits = Habit.objects.all()
	return render(request, 'dashboard.html', {'habits': habits})

# Dashboard - Habits Detail View
def habits_detail(request, habit_id):
	habit = Habit.objects.get(id=habit_id)
	return render(request, 'habits/detail.html', { 'habit': habit })

# Inspo View
def inspo(request):
	return render(request, 'inspo.html')


# Logout View
def logout(request):
	return render(request, 'logout.html')


# Class Based Views (CBVs) =====================

# Create Habit
class HabitCreate(CreateView):
	model = Habit
	fields = '__all__'
	success_url = '/dashboard/'

# Update Habit
class HabitUpdate(UpdateView):
	model = Habit
	fields = ['healthy', 'plan_of_action', 'external_cue', 'internal_cue']

# Delete Habit
class HabitDelete(DeleteView):
	model = Habit
	success_url = '/dashboard/'