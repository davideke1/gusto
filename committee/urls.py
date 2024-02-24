# from django.urls import path
# from .views import custom_login,landing_page,all_colleges, all_payments, all_captains,all_complain,all_team

# urlpatterns = [
#     path('login/', custom_login, name='login'),
#     # path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
#     path('landing/', landing_page, name='landing_page'),

#     path('all_colleges/', all_colleges, name='all_colleges'),
#     path('all_payments/', all_payments, name='all_payments'),
#     path('all_team/', all_team, name='all_team'),
#     path('all_captains/', all_captains, name='all_captains'),
#     path('all_complain/', all_complain, name='all_complain'),
#     # path('poc/dashboard/<str:sport>/', poc_dashboard, name='poc_dashboard'),


#     #poc links
# ]

from django.urls import path
from .views import AllCollegesView, AllTeamView, AllComplaintsView, AllCaptainsView, AllPaymentsView,custom_login, LandingPageView


urlpatterns = [
     path('login/', custom_login, name='login'),
    path('', LandingPageView.as_view(), name='landing_page'),
    path('all_colleges/', AllCollegesView.as_view(), name='all_colleges'),
    path('all_team/', AllTeamView.as_view(), name='all_team'),
    path('all_complain/', AllComplaintsView.as_view(), name='all_complain'),
    path('all_captains/', AllCaptainsView.as_view(), name='all_captains'),
    path('all_payments/', AllPaymentsView.as_view(), name='all_payments'),
    # Add other URLs as needed
]
