from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import SignUpView

urlpatterns = [
    path('accounts/signup/', views.SignUpView, name='signup'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/login/', auth_views.LoginView.as_view(), name="login"),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('about_us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('tournaments_list/', views.tournaments_list, name='tournaments_list'),
    path('referee/', views.referee_landing, name='referee_landing'),
    path('coach/', views.coach_landing, name='coach_landing'),
    path('login_landing/', views.login_landing, name='login_landing'),
    path('matches_list/<int:pk>/', views.matches_list, name='matches_list'),
    path('matches/create/', views.matches_new, name='matches_new'),
    path('referee/matches_list/', views.referee_matches_list, name='referee_matches_list'),
    path('referee/matches/<int:pk>/edit/', views.referee_matches_edit, name='referee_matches_edit'),
    path('referee/matches/<int:pk>/delete/', views.referee_matches_delete, name='referee_matches_delete'),
    path('referee/matches/<int:match_ID>/scores_report/', views.scores_report, name='scores_report'),
    path('referee/matches/scores_report/success', views.successView, name='successView'),
    path('referee/scores_report/success', views.successView, name='successView'),
    path('players_list', views.players_list, name='players_list'),
    path('players/create/', views.players_new, name='players_new'),
    path('players/<int:pk>/edit/', views.players_edit, name='players_edit'),
    path('players/<int:pk>/delete/', views.players_delete, name='players_delete'),
    path('coach/players_list', views.coach_players_list, name='coach_players_list'),
    path('coach/players/create/', views.coach_players_new, name='coach_players_new'),
    path('coach/players/<int:pk>/edit/', views.coach_players_edit, name='coach_players_edit'),
    path('coach/players/<int:pk>/delete/', views.coach_players_delete, name='coach_players_delete'),
    path('coach/summary', views.team_summary, name='coach_team_summary'),
    path('schools_list/', views.schools_list, name='schools_list'),
    path('teams_list/<int:pk>/', views.teams_list, name='teams_list'),
    path('players_list/<int:pk>/', views.players_list, name='players_list'),
    path('admin/match/<int:match_ID>/pdf/', views.admin_match_pdf, name='admin_match_pdf'),
]
