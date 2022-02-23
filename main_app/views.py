from dataclasses import fields
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Habit
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Views
# ========================================================

# Welcome/Login View
def login(request):
	return render(request, 'registration/login.html')

# Signup View
def signup(request):
	error_message = ''
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('/dashboard')
		else:
			error_message = 'Invalid Sign Up - Please try again'
	form = UserCreationForm()
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
	habit = Habit.objects.get(id=habit_id)
	return render(request, 'habits/detail.html', { 'habit': habit })

# Inspo View
@login_required
def inspo(request):
	return render(request, 'inspo.html')


# Logout View
@login_required
def logout(request):
	return render(request, 'logout.html')


# Class Based Views (CBVs) =====================

# Create Habit
class HabitCreate(LoginRequiredMixin, CreateView):
	model = Habit
	fields = ['habit_name', 'healthy', 'plan_of_action', 'external_cue', 'internal_cue']
	success_url = '/dashboard/'

	# User model validation
	def form_vaild(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

# Update Habit
class HabitUpdate(LoginRequiredMixin, UpdateView):
	model = Habit
	fields = ['healthy', 'plan_of_action', 'external_cue', 'internal_cue']
	def dispatch(self, request, *args, **kwargs):
		obj = self.get_object()
		if obj.user != self.request.user:
			return redirect('accounts/login/')
		return super(HabitUpdate, self).dispatch(request, *args, **kwargs)

# Delete Habit
class HabitDelete(LoginRequiredMixin, DeleteView):
	model = Habit
	success_url = '/dashboard/'
	def dispatch(self, request, *args, **kwargs):
		obj = self.get_object()
		if obj.user != self.request.user:
			return redirect('accounts/login/')
		return super(HabitUpdate, self).dispatch(request, *args, **kwargs)