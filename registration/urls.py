from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('qarrj-hasana-register/', views.qarrj_hasana_register, name='qarrj_hasana_register'),
    #  path('register-mosque/', views.mosque_registration, name='mosque_registration'),
    #  path('xx', views.mosque_registration, name='mosque_registration'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)