from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('event/', views.event, name='event'),
    path('complains/', views.complains, name='complain'),
    path('core-team/', views.coreteam, name='coreteam'),
    path('register/', views.register, name='register'),
    path('gallery/', views.gallery, name='gallery'),
]
