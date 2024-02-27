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
    path('upload/', views.team_member_upload, name='team_member_upload'),

    # blogger
    path('game/', views.GameResultListView.as_view(), name='game_result_list'),
    path('game/create/', views.GameResultCreateView.as_view(), name='game_result_create'),
    path('game/<int:pk>/update/', views.GameResultUpdateView.as_view(), name='game_result_update'),
    path('game/<int:pk>/delete/', views.GameResultDeleteView.as_view(), name='game_result_delete'),
    path('game/<int:pk>/', views.GameResultDetailView.as_view(), name='game_result_detail'),
    path('blogger-login/', views.BloggerLoginView.as_view(), name='blogger_login'),
    path("logout/", views.logout_request, name="logout"),
]

