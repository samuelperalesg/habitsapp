from django import forms
from .models import Habit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['habit_name', 'healthy', 'plan_of_action', 'external_cue', 'internal_cue']
