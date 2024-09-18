from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register-mosque/', views.mosque_registration, name='mosque_registration'),
    path('qarrj-hasana-register/', views.qarrj_hasana_register, name='qarrj_hasana_register'),

]
