from django.core.management.base import BaseCommand
from main_app.models import Habit, Day
from django.contrib.auth.models import User
import datetime
import random

class Command(BaseCommand):
    help = 'Populate the database with fake data for user=daniel'

    def handle(self, *args, **kwargs):

        # Assuming 'daniel' user exists, if not you should create it first
        user = User.objects.get(username='daniel')

        # Some sample data for habits
        habits_data = [
            {'name': 'Morning Run', 'healthy': True, 'plan': 'Run every morning at 6 AM', 'external': 'Alarm at 6', 'internal': 'Feeling of freshness'},
            {'name': 'Evening Snack', 'healthy': False, 'plan': 'Avoid eating junk food', 'external': 'Hunger pangs', 'internal': 'Avoiding health issues'},
            {'name': 'Meditation', 'healthy': True, 'plan': 'Meditate for 10 minutes', 'external': 'Meditation App Reminder', 'internal': 'Peace and calm'},
            {'name': 'Late-night work', 'healthy': False, 'plan': 'Try to finish work by 9 PM', 'external': 'Work emails', 'internal': 'Needing rest and sleep'},
        ]

        # Populate habits for daniel
        for habit_data in habits_data:
            Habit.objects.get_or_create(
                habit_name=habit_data['name'],
                healthy=habit_data['healthy'],
                plan_of_action=habit_data['plan'],
                external_cue=habit_data['external'],
                internal_cue=habit_data['internal'],
                user=user
            )

        # Populate days and habits_completed for daniel
        for i in range(1, 31):  # Let's create entries for 30 days
            date = datetime.date.today() - datetime.timedelta(days=i)
            day, created = Day.objects.get_or_create(date=date, user=user)

            # Randomly associate some habits with the day
            for habit in Habit.objects.filter(user=user).order_by('?')[:random.randint(1, 4)]:  # Choose 1-4 habits randomly
                day.habits_completed.add(habit)

            # Color logic, can be expanded or refined further
            healthy_habits = day.habits_completed.filter(healthy=True)
            if healthy_habits.count() == Habit.objects.filter(user=user, healthy=True).count():
                day.color_status = '#B3FFB3'  # Green
            elif healthy_habits.count() >= 1:
                day.color_status = '#FFFFB3'  # Yellow
            else:
                day.color_status = '#FFB3B3'  # Red
            day.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated data for user=daniel'))
