from django.db import models

# Habit Model

class Habit(models.Model):
	habit_name = models.CharField(max_length=100)
	healthy = models.BooleanField()
	plan_of_action = models.TextField(max_length=250)
	external_cue = models.CharField(max_length=100)
	internal_cue = models.CharField(max_length=100)
