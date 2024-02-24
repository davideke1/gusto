# # main/views.py
# from django.contrib.auth import authenticate, login
# from django.shortcuts import render, redirect
# from main.models import College, Payment, Sport, Team, SportInformation, Complaint, TeamCaptain
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.contrib import messages

# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.shortcuts import render, redirect

# def custom_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)

#         if user is not None and user.check_password(password):
#             # Password is correct, log in the user and redirect
#             login(request, user)
#             return redirect('landing_page')  # Change to your appropriate view
#         else:
#             # Display an error message for invalid password
#             messages.error(request, 'Invalid username or password. Please try again.')

#     # Re-render the login page with the error message
#     return render(request, 'login.html')



# @login_required
# def landing_page(request):
#     top_colleges = College.objects.all()[:5]
#     top_payments = Payment.objects.all()[:5]
#     top_teams = Team.objects.all()[:5]
    
#     top_complaints = Complaint.objects.all()[:5]
#     top_team_captains = TeamCaptain.objects.all()[:5]

#     context = {
#         'top_colleges': top_colleges,
#         'top_payments': top_payments,
#         'top_teams': top_teams,
#         'top_complaints': top_complaints,
#         'top_team_captains': top_team_captains,
#     }

#     return render(request, 'admin_dashboard.html', context)


# #admin  views
# @login_required
# def all_colleges(request):
#     colleges = College.objects.all()
#     return render(request, 'all_colleges.html', {'colleges': colleges})


# @login_required
# def all_team(request):
#     # Get all colleges with related teams and sports
#     all_colleges = College.objects.all()

#     # Handle search query
#     search_query = request.GET.get('search', '')
#     if search_query:
#         all_colleges = all_colleges.filter(name__icontains=search_query)

#     context = {'all_colleges': all_colleges, 'search_query': search_query}
#     return render(request, 'all_team.html', context)
    

#     # # Pass the colleges to the template
#     # return render(request, 'all_team.html', {'all_colleges': all_colleges})
# @login_required
# def all_complain(request):
#     # Retrieve all sports for the dropdown filter
#     all_sports = Sport.objects.all()

#     # Retrieve all complaints
#     complaints_list = Complaint.objects.all()

#     # Apply filtering based on selected sport, if any
#     selected_sport = request.GET.get('sport')
#     if selected_sport and selected_sport != 'all':
#         complaints_list = complaints_list.filter(sport__name=selected_sport)

#     # Number of complaints to display per page
#     complaints_per_page = 3

#     paginator = Paginator(complaints_list, complaints_per_page)
#     page = request.GET.get('page')

#     try:
#         complaints = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver the first page
#         complaints = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range (e.g. 9999), deliver the last page
#         complaints = paginator.page(paginator.num_pages)

#     return render(request, 'all_complain.html', {'complaints': complaints, 'all_sports': all_sports, 'selected_sport': selected_sport})

# @login_required
# def all_captains(request):
#     # Retrieve all sports for the dropdown filter
#     all_sports = Sport.objects.all()

#     # Retrieve all team captains
#     captains_list = TeamCaptain.objects.all()

#     # Apply filtering based on selected sport, if any
#     selected_sport = request.GET.get('sport')
#     if selected_sport and selected_sport != 'all':
#         captains_list = captains_list.filter(sport__name=selected_sport)

#     # Number of captains to display per page
#     captains_per_page = 3

#     paginator = Paginator(captains_list, captains_per_page)
#     page = request.GET.get('page')

#     try:
#         captains = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver the first page
#         captains = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range (e.g. 9999), deliver the last page
#         captains = paginator.page(paginator.num_pages)

#     return render(request, 'all_captain.html', {'captains': captains, 'all_sports': all_sports, 'selected_sport': selected_sport})

# @login_required
# def all_payments(request):
#     # Retrieve all college for the dropdown filter
#     all_colleges = College.objects.all()

#     payments_list = Payment.objects.all()

#     # Handle form submission
#     selected_college = request.GET.get('college')
#     if selected_college and selected_college != 'all':
#         payments_list = payments_list.filter(college__name=selected_college)  # Corrected this line

#     # Number of payments to display per page
#     payments_per_page = 3

#     paginator = Paginator(payments_list, payments_per_page)
#     page = request.GET.get('page')

#     try:
#         payments = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver the first page
#         payments = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range (e.g. 9999), deliver the last page
#         payments = paginator.page(paginator.num_pages)

#     context = {'payments': payments, 'all_colleges': all_colleges, 'selected_college': selected_college}
#     return render(request, 'all_payments.html', context)
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from main.models import College, Payment, Sport, Team, SportInformation, Complaint, TeamCaptain
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Get the 'next' parameter from the URL
            next_param = request.GET.get('next')

            # If 'next' is not present in the URL, try to resolve it from the path
            if not next_param:
                try:
                    # Get the resolved view name for the current path
                    match = resolve(request.path_info)
                    next_param = match.url_name
                except:
                    pass  # Handle the exception as needed

            # Redirect to the 'next' parameter if present, otherwise redirect to a default page
            return redirect(next_param) if next_param else redirect('landing_page')
        else:
            # Display an error message for invalid login
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'login.html')

class LandingPageView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_dashboard.html'

    def get_context_data(self, **kwargs):
        top_colleges = College.objects.all()[:5]
        top_payments = Payment.objects.all()[:5]
        top_teams = Team.objects.all()[:5]
        top_complaints = Complaint.objects.all()[:5]
        top_team_captains = TeamCaptain.objects.all()[:5]

        context = {
            'top_colleges': top_colleges,
            'top_payments': top_payments,
            'top_teams': top_teams,
            'top_complaints': top_complaints,
            'top_team_captains': top_team_captains,
        }

        return context
@method_decorator(login_required, name='dispatch')
class AllCollegesView(TemplateView):
    template_name = 'all_colleges.html'

    def get_context_data(self, **kwargs):
        colleges = College.objects.all()
        return {'colleges': colleges}

@method_decorator(login_required, name='dispatch')
class AllTeamView(TemplateView):
    template_name = 'all_team.html'

    def get_context_data(self, **kwargs):
        all_colleges = College.objects.all()

        search_query = self.request.GET.get('search', '')
        if search_query:
            all_colleges = all_colleges.filter(name__icontains=search_query)

        context = {'all_colleges': all_colleges, 'search_query': search_query}
        return context

@method_decorator(login_required, name='dispatch')
class AllComplaintsView(TemplateView):
    template_name = 'all_complain.html'

    def get_context_data(self, **kwargs):
        all_sports = Sport.objects.all()
        complaints_list = Complaint.objects.all()

        selected_sport = self.request.GET.get('sport')
        if selected_sport and selected_sport != 'all':
            complaints_list = complaints_list.filter(sport__name=selected_sport)

        complaints_per_page = 3

        paginator = Paginator(complaints_list, complaints_per_page)
        page = self.request.GET.get('page')

        try:
            complaints = paginator.page(page)
        except PageNotAnInteger:
            complaints = paginator.page(1)
        except EmptyPage:
            complaints = paginator.page(paginator.num_pages)

        context = {'complaints': complaints, 'all_sports': all_sports, 'selected_sport': selected_sport}
        return context

@method_decorator(login_required, name='dispatch')
class AllCaptainsView(TemplateView):
    template_name = 'all_captain.html'

    def get_context_data(self, **kwargs):
        all_sports = Sport.objects.all()
        captains_list = TeamCaptain.objects.all()

        selected_sport = self.request.GET.get('sport')
        if selected_sport and selected_sport != 'all':
            captains_list = captains_list.filter(sport__name=selected_sport)

        captains_per_page = 3

        paginator = Paginator(captains_list, captains_per_page)
        page = self.request.GET.get('page')

        try:
            captains = paginator.page(page)
        except PageNotAnInteger:
            captains = paginator.page(1)
        except EmptyPage:
            captains = paginator.page(paginator.num_pages)

        context = {'captains': captains, 'all_sports': all_sports, 'selected_sport': selected_sport}
        return context

@method_decorator(login_required, name='dispatch')
class AllPaymentsView(TemplateView):
    template_name = 'all_payments.html'

    def get_context_data(self, **kwargs):
        all_colleges = College.objects.all()
        payments_list = Payment.objects.all()

        selected_college = self.request.GET.get('college')
        if selected_college and selected_college != 'all':
            payments_list = payments_list.filter(college__name=selected_college)

        payments_per_page = 3

        paginator = Paginator(payments_list, payments_per_page)
        page = self.request.GET.get('page')

        try:
            payments = paginator.page(page)
        except PageNotAnInteger:
            payments = paginator.page(1)
        except EmptyPage:
            payments = paginator.page(paginator.num_pages)

        context = {'payments': payments, 'all_colleges': all_colleges, 'selected_college': selected_college}
        return context
