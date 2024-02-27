from datetime import date
from django.forms.widgets import DateInput
from django import forms
from .models import College, Payment, Sport,ContactMessage, Complaint, TeamCaptain,GameResult,TeamMember

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['reference_code', 'amount', 'payment_date']

        widgets = {
            'reference_code': forms.TextInput(attrs={
                'class': 'form-control form-control-lg bg-light fs-6 text-white',
                'placeholder': 'Enter payment transaction ID',
                'required': 'required',
            }),
            'amount': forms.TextInput(attrs={
                'class': 'form-control form-control-lg bg-light fs-6 text-white',
                'placeholder': 'Enter Amount',
                'readonly': 'readonly',
                'required': 'required',
            }),
            'payment_date': forms.TextInput(attrs={
                'class': 'form-control form-control-lg bg-light fs-6 text-white',
                'type': 'date',
                'required': 'required',
                
                'value': date.today().strftime('%Y-%m-%d'),
            })
        }

class TeamCaptainForm(forms.ModelForm):
    class Meta:
        model = TeamCaptain
        fields = ['captain_name', 'phone']  # Change 'name' to 'captain_name'
        widgets = {
            'captain_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg bg-light fs-6 text-white',
                'placeholder': 'Enter Team Captain Name',
                'required': 'required',
                'type': 'text'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control form-control-lg bg-light fs-6 text-white',
                'placeholder': 'Enter Team Captain Phone Number',
                'required': 'required',
                'type': 'tel',
            }),
        }


class RegistrationForm(forms.ModelForm):
    sport = forms.ModelChoiceField(
        queryset=Sport.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select form-select-lg bg-light fs-6 text-white',
            'required': 'required',
            'id': 'id_sport',
        }),
        required=True,
    )

    

    # team_captain_form = TeamCaptainForm()  # Instantiate TeamCaptainForm

    class Meta:
        model = College
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg bg-light fs-6 text-white',
                'placeholder': 'Enter College Name',
                'required': 'required',
                'type': 'text'
            }),
        }

    def save(self, commit=True):
        name = self.cleaned_data['name']

        # Get the college or create a new one
        college, created = College.objects.get_or_create(name=name)

        # Associate the selected sport with the college
        if 'sport' in self.cleaned_data and self.cleaned_data['sport']:
            college.sports.add(self.cleaned_data['sport'])

        # Create a new TeamCaptainForm instance with the POST data
        team_captain_form = TeamCaptainForm(self.cleaned_data)
        if team_captain_form.is_valid():
            team_captain = team_captain_form.save(commit=False)
            team_captain.college = college
            team_captain.sport = self.cleaned_data['sport']
            if commit:
                team_captain.save()
                print('Team Captain saved')

        # Save the payment using PaymentForm
        payment_form = PaymentForm(self.cleaned_data)
        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.college = college
            if commit:
                payment.save()
                print('Payment saved')

        return college


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']

        widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name *',id:"name", 'data-sb-validations': 'required'}),
        'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email *',type:"email",id:"email", 'data-sb-validations': 'required'}),
        'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone *', id:"phone", type:"tel", 'data-sb-validations': 'required'}),
        'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message *',  id:"message",'data-sb-validations': 'required'}),
    }


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['name', 'phone', 'email', 'college', 'category', 'complaint']

    widgets = {
        'name': forms.TextInput(attrs={
            'class': 'form-control form-control-lg bg-light fs-6',
            'placeholder': 'Enter Name',
            'required': 'required',
            'type': 'text'
        }),
        'phone': forms.TextInput(attrs={
            'class': 'form-control form-control-lg bg-light fs-6',
            'placeholder': 'Enter Phone Number',
            'required': 'required',
            'type': 'tel',
        }),
        'email': forms.TextInput(attrs={
            'class': 'form-control form-control-lg bg-light fs-6',
            'placeholder': 'Enter email',
            'required': 'required',
            'type': 'email',
        }),
        'college': forms.TextInput(attrs={
            'class': 'form-control form-control-lg bg-light fs-6',
            'placeholder': 'Enter College',
            'required': 'required',
            'type': 'text',
        }),
        'category': forms.Select(attrs={
            'class': 'form-control form-control-lg bg-light fs-6',
            'required': 'required',
        }),
        'complaint': forms.Textarea(attrs={
            'class': 'form-control form-control-lg bg-light fs-6',
            'placeholder': 'Make your complains',
            'required': 'required',
        }),
    }

    def __init__(self, *args, **kwargs):
        super(ComplaintForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Sport.objects.all()


class GameResultForm(forms.ModelForm):
    class Meta:
        model = GameResult
        fields = ['sport','team_a', 'team_b', 'score_a', 'score_b', 'result']

    def __init__(self, *args, **kwargs):
        super(GameResultForm, self).__init__(*args, **kwargs)
        self.fields['team_a'].widget.attrs['placeholder'] = 'Team A'
        self.fields['team_b'].widget.attrs['placeholder'] = 'Team B'
        # Add similar placeholder attributes for other fields if needed

    def clean(self):
        cleaned_data = super().clean()
        # Add any additional validation logic here
        return cleaned_data
    
class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'image', 'instagram_profile', 'mail_profile', 'linkedin_profile']
