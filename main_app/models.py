from audioop import reverse
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Habit Model

class Habit(models.Model):
	habit_name = models.CharField(max_length=100)
	healthy = models.BooleanField()
	plan_of_action = models.TextField(max_length=200)
	external_cue = models.TextField(max_length=200)
	internal_cue = models.TextField(max_length=200)
	
	# User Model
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.habit_name

	def get_absolute_url(self):
		return reverse('detail', kwargs={'habit_id': self.id})
