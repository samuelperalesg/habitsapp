from django.urls import path
from . import views

urlpatterns = [
	path('', views.welcome, name='welcome'),
	path('signup/', views.signup, name='signup'),
	path('dashboard/', views.dashboard, name='dashboard'),
	path('habits/<int:habit_id>/', views.habits_detail, name='detail'),
	path('add/', views.HabitCreate.as_view(), name='add'),
	path('inspo/', views.inspo, name='inspo'),
	path('logout/', views.logout, name='logout'),
]