from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register-mosque/', views.mosque_registration, name='mosque_registration'),
]
