from django.shortcuts import render
from django.http import HttpResponse

# Views
# ========================================================

# Welcome View
def welcome(request):
	return render(request, 'welcome.html')

# Signup View
def signup(request):
	return render(request, 'signup.html')

# Dashboard View
def dashboard(request):
	return render(request, 'dashboard.html', {'habits': habits})

# Inspo View
def inspo(request):
	return render(request, 'inspo.html')

# Add_edit View
def add_edit(request):
	return render(request, 'add_edit.html')

# Logout View
def logout(request):
	return render(request, 'logout.html')

# Models
# ========================================================

class Habit:
	def __init__(self, habit_name, healthy, plan_of_action, external_cue, internal_cue):
		self.habit_name = habit_name
		self.healthy = healthy
		self.plan_of_action = plan_of_action
		self.external_cue = external_cue
		self.internal_cue = internal_cue

habits = [
	Habit('Brushing Teeth', 'True', 'none', 'Teeth feel dirty', 'I want to have a pretty smile'),
]