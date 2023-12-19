from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('habits/<int:habit_id>/', views.habits_detail, name='detail'),
    path('add/', views.HabitCreate.as_view(), name='add'),
    path('<int:pk>/update/', views.HabitUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', views.HabitDelete.as_view(), name='delete'),
    path('inspo/', views.inspo, name='inspo'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update_habit/<int:habit_id>/', views.update_habit, name='update_habit'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('day/<str:date>/', views.day_detail_view, name='day_detail_view'),
    path('add_to_calendar/', views.add_to_calendar, name='add_to_calendar'),
    path('guest_login/', views.guest_login, name='guest_login'),
]
