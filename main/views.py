from django.shortcuts import render, redirect
from .forms import  RegistrationForm, PaymentForm,ContactForm,ComplaintForm
from .models import College, Team, Sport, Payment,CarouselSlide, TeamMember,SportInformation
from django.shortcuts import render
from django.contrib import messages


from django.shortcuts import render, redirect

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

def gallery(request):
    return render(request, 'features/test1.html')



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
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        payment_form = PaymentForm(request.POST)

        if registration_form.is_valid() and payment_form.is_valid():
            college = registration_form.save(commit=False)
            college.save()

            payment = payment_form.save(commit=False)
            payment.college = college
            payment.save()

            # Redirect to a success page or do something else
            return redirect('home')

    else:
        registration_form = RegistrationForm()
        payment_form = PaymentForm()

    return render(request, 'features/register.html', {'registration_form': registration_form, 'payment_form': payment_form})


from django.shortcuts import render


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)