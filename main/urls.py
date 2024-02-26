from django.urls import path
from . import views

urlpatterns = [
    path('', views.splash_screen, name='splash'),
    path('home', views.home, name='home'),
    path('event/', views.event, name='event'),
    path('complains/', views.complains, name='complain'),
    path('core-team/', views.coreteam, name='coreteam'),
    path('register/', views.register, name='register'),
    # path('gallery/', views.gallery, name='gallery'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('term-of-use/', views.termofuse, name='termofuse'),
    path('results/', views.result, name='result'),
]
