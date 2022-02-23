from django.urls import path
from . import views

urlpatterns = [
	path('accounts/login', views.login, name='login'),
	path('signup/', views.signup, name='signup'),
	path('dashboard/', views.dashboard, name='dashboard'),
	path('habits/<int:habit_id>/', views.habits_detail, name='detail'),
	path('add/', views.HabitCreate.as_view(), name='add'),
	path('<int:pk>/update/', views.HabitUpdate.as_view(), name='update'),
	path('<int:pk>/delete/', views.HabitDelete.as_view(), name='delete'),
	path('inspo/', views.inspo, name='inspo'),
	path('logout/', views.logout, name='logout'),
	path('accounts/signup', views.signup, name='signup')
]