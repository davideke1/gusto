from datetime import date
from django.forms.widgets import DateInput
from django import forms
from .models import College, Payment, Sport,ContactMessage, Complaint

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['reference_code', 'amount', 'payment_date']

        widgets = {
            'reference_code': forms.TextInput(attrs={
                'class': 'form-control form-control-lg bg-light fs-6',
                'placeholder': 'Enter payment transaction ID',
                'required': 'required',
            }),
            'amount': forms.TextInput(attrs={
                'class': 'form-control form-control-lg bg-light fs-6',
                'placeholder': 'Enter Amount',
                'required': 'required',
            }),
            'payment_date': forms.TextInput(attrs={
                'class': 'form-control form-control-lg bg-light fs-6',
                'type': 'date',
                'required': 'required',
                'value': date.today().strftime('%Y-%m-%d'),
            })
        }
        
class RegistrationForm(forms.ModelForm):
    sport = forms.ModelChoiceField(
        queryset=Sport.objects.all(),
        widget=forms.Select(attrs={
            'class':'form-select form-select-lg bg-light fs-6',
            'required':'required',
            'id': 'id_sport',
            
        }),
        required=True,
    )

    class Meta:
        model = College
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg bg-light fs-6',
                'placeholder': 'Enter College Name',
                'required': 'required',
                'type' : 'text'
            }),
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Add a disabled option for the 'sport' field
    #     self.fields['sport'].widget.choices = [('', 'Select Sport (Disabled)')] + list(self.fields['sport'].widget.choices)[1:]
    #     self.fields['sport'].widget.attrs.update({'disabled': 'disabled'})

    def save(self, commit=True):
        name = self.cleaned_data['name']

        # Get the college or create a new one
        college, created = College.objects.get_or_create(name=name)

        # Associate the selected sport with the college
        if 'sport' in self.cleaned_data and self.cleaned_data['sport']:
            college.sports.add(self.cleaned_data['sport'])

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

    def __init__(self, *args, **kwargs):
        super(ComplaintForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Sport.objects.all()
