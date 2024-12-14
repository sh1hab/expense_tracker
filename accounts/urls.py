from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    
    # Django's built-in authentication views
    path('login/', 
         auth_views.LoginView.as_view(template_name='login.html'), 
         name='login'),
    path('logout/', 
         auth_views.LogoutView.as_view(next_page='accounts:login'), 
         name='logout'),
    
    # Password reset views
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html',
             email_template_name='accounts/password_reset_email.html',
             success_url='/accounts/password-reset/done/'
         ), 
         name='password_reset'),

    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ), 
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),

    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]