from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('register/', views.register, name='register'),
  path('login/', LoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(next_page = settings.LOGOUT_REDIRECT_URL), name='logout'),
  path('tasks/', views.task_list, name='task_list'),
  path('tasks/create/', views.task_create, name='task_create'),
  path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
  path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
  path('tasks/<int:pk>/toggle', views.task_toggle_status, name='task_toggle_status'),
  path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
  path('password_reset/done/',  views.PasswordResetDoneView.as_view(), name='password_reset_done'),
  path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
  path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
  path('profile/', views.profile, name='profile'),
  path('profile/edit/', views.edit_profile, name='profile_edit'),
  path('password_change/', views.change_password, name='password_change'),
  path('password_change/done/', views.change_password_done, name='password_change_done'),
  path('reminder/', views.reminder, name='reminder'),
  path('tasks/<int:pk>/', views.task_detail, name='task_detail'),

]