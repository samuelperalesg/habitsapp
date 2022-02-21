from django.urls import path
from . import views

urlpatterns = [
	path('', views.welcome, name='welcome'),
	path('signup', views.signup, name='signup'),
	path('dashboard', views.dashboard, name='dashboard'),
	path('inspo', views.inspo, name='inspo'),
	path('add_edit', views.add_edit, name='add_edit'),
	path('logout', views.logout, name='logout'),
]