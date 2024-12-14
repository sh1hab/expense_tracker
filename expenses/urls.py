# expenses/urls.py
from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),

    path('analytics', views.analytics, name='analytics'),

]

