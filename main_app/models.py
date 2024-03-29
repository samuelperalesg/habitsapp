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
	is_done = models.BooleanField(default=False)
	
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.habit_name

	def get_absolute_url(self):
		return reverse('detail', kwargs={'habit_id': self.id})

class Day(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habits_completed = models.ManyToManyField(Habit, related_name='completed_habits')
    color_status = models.CharField(max_length=100, null=True, blank=True)
				
    class Meta:
        unique_together = [['user', 'date']]
