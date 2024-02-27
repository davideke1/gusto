from django.shortcuts import render, redirect
from .forms import  RegistrationForm, PaymentForm,ContactForm,ComplaintForm,TeamCaptainForm,GameResultForm,TeamMemberForm
from .models import College, Team, Sport, Payment,CarouselSlide, TeamMember,SportInformation,GameResult
from django.contrib import messages
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

def home(request):
    # Query all CarouselSlide objects from the database
    carousel_slides = CarouselSlide.objects.all()

    # Pass the queryset to the template context
    context = {'carousel_slides': carousel_slides}

    # Render the template with the context
    return render(request, 'features/home.html', context)

def event(request):
    sports_info = SportInformation.objects.all()
    context = {'sports_info': sports_info}
    return render(request, 'features/event.html', context)

# def teams(request):
#     return render(request, 'features/teams.html')

def coreteam(request):
    team_members = TeamMember.objects.all()
    return render(request, 'features/coreteam.html', {'team_members': team_members})

# def complains(request):
#     return render(request, 'features/complain.html')

# def register(request):
#     return render(request, 'features/register.html')

def privacy_policy(request):
    return render(request, 'features/privacy.html')

def termofuse(request):
    return render(request, 'features/termofuse.html')

def splash_screen(request):
    return render(request, 'intro.html')

# def result(request):
#     return render(request,"features/results.html")

# def result(request):
#     sports = Sport.objects.all()
#     game_results = GameResult.objects.all()

#     context = {
#         'sports': sports,
#         'game_results': game_results,
#     }

#     return render(request, 'features/results.html', context)

def result(request):
    sports = Sport.objects.all()
    game_results = GameResult.objects.all()

    # Number of items per page
    items_per_page = 10
    paginator = Paginator(game_results, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the requested page
        game_results = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, default to the first page
        game_results = paginator.page(1)
    except EmptyPage:
        # If the requested page is out of range (e.g., 9999), deliver the last page
        game_results = paginator.page(paginator.num_pages)

    context = {
        'sports': sports,
        'game_results': game_results,
    }

    return render(request, 'features/results.html', context)

def complains(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'features/complain_success.html')
    else:
        form = ComplaintForm()

    return render(request, 'features/complain.html', {'form': form})

def teams(request):
    sports = Sport.objects.all()
    selected_sport = request.GET.get('sport', '')

    if selected_sport:
        teams = Team.objects.filter(sport__name=selected_sport)
    else:
        teams = Team.objects.all()

    return render(request, 'features/teams.html', {'teams': teams, 'sports': sports, 'selected_sport': selected_sport})


def register(request):
    sport_amounts = {sport.name: str(sport.sport_amount) for sport in Sport.objects.all()}
    
    # Convert to JSON format
    sport_amounts_json = json.dumps(sport_amounts, cls=DjangoJSONEncoder)
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        payment_form = PaymentForm(request.POST)
        team_captain_form = TeamCaptainForm(request.POST)
        
        if registration_form.is_valid() and payment_form.is_valid() and team_captain_form.is_valid():
            college = registration_form.save(commit=False)
            college.save()

            # Save the team captain using TeamCaptainForm
            team_captain = team_captain_form.save(commit=False)
            team_captain.college = college  # Set college attribute to the actual College instance
            team_captain.sport = registration_form.cleaned_data['sport']
            team_captain.save()


            payment = payment_form.save(commit=False)
            payment.college = college
            payment.save()

            # Redirect to a success page or do something else
            return redirect('home')

    else:
        registration_form = RegistrationForm()
        payment_form = PaymentForm()
        team_captain_form = TeamCaptainForm()

    return render(request, 'features/register.html', {'registration_form': registration_form, 'payment_form': payment_form, 'team_captain_form': team_captain_form, 'sport_amounts': sport_amounts_json})


# def register(request):
#     if request.method == 'POST':
#         registration_form = RegistrationForm(request.POST)
#         payment_form = PaymentForm(request.POST)

#         if registration_form.is_valid() and payment_form.is_valid():
#             college = registration_form.save(commit=False)
#             college.save()

#             payment = payment_form.save(commit=False)
#             payment.college = college
#             payment.save()

#             # Redirect to a success page or do something else
#             return redirect('home')

#     else:
#         registration_form = RegistrationForm()
#         payment_form = PaymentForm()

#     return render(request, 'features/register.html', {'registration_form': registration_form, 'payment_form': payment_form})

def error_404(request, exception):
    return render(request, '404.html', status=404)
 
def error_500(request):
    return render(request, '500.html', status=500)


def game_result_list(request):
    game_results = GameResult.objects.all()
    return render(request, 'game_result_list.html', {'game_results': game_results})

def game_result_detail(request, pk):
    game_result = get_object_or_404(GameResult, pk=pk)
    return render(request, 'game_result_detail.html', {'game_result': game_result})

def game_result_create(request):
    if request.method == 'POST':
        form = GameResultForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('game_result_list')
    else:
        form = GameResultForm()
    return render(request, 'game_result_form.html', {'form': form})

def game_result_update(request, pk):
    game_result = get_object_or_404(GameResult, pk=pk)
    form = GameResultForm(request.POST or None, instance=game_result)
    if form.is_valid():
        form.save()
        return redirect('game_result_list')
    return render(request, 'game_result_form.html', {'form': form})

def game_result_delete(request, pk):
    game_result = get_object_or_404(GameResult, pk=pk)
    if request.method == 'POST':
        game_result.delete()
        return redirect('game_result_list')
    return render(request, 'game_result_confirm_delete.html', {'game_result': game_result})


def team_member_upload(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('coreteam')  # Redirect to a page showing the list of team members
    else:
        form = TeamMemberForm()

    return render(request, 'features/team_member_upload.html', {'form': form})

class BloggerLoginView(LoginView):
    template_name = 'blogger/blogger_login.html'  # Specify the template for the login page
    success_url = reverse_lazy('game_result_list')  # Redirect to this URL after successful login

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # You can add additional context data if needed
        return context

class GameResultListView(LoginRequiredMixin, ListView):
    model = GameResult
    template_name = 'blogger/game_result_list.html'
    context_object_name = 'game_results'
    login_url = '/blogger-login/'  # Specify the blogger login URL

class GameResultCreateView(LoginRequiredMixin, CreateView):
    model = GameResult
    form_class = GameResultForm
    template_name = 'blogger/game_result_form.html'
    success_url = reverse_lazy('game_result_list')
    login_url = '/blogger-login/'

class GameResultUpdateView(LoginRequiredMixin, UpdateView):
    model = GameResult
    form_class = GameResultForm
    template_name = 'blogger/game_result_form.html'
    success_url = reverse_lazy('game_result_list')
    login_url = '/blogger-login/'

class GameResultDeleteView(LoginRequiredMixin, DeleteView):
    model = GameResult
    template_name = 'blogger/game_result_confirm_delete.html'
    success_url = reverse_lazy('game_result_list')
    login_url = '/blogger-login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game_result'] = self.get_object()
        return context

class GameResultDetailView(LoginRequiredMixin, DetailView):
    model = GameResult
    template_name = 'blogger/game_result_detail.html'
    context_object_name = 'game_result'
    login_url = '/blogger-login/'