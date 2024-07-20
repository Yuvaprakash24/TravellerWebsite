from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import User,Contact,BookTrip,TripQueries

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['msg','name','email','sub']

class BookTripForm(forms.ModelForm):
    class Meta:
        model=BookTrip
        fields=['destination', 'tourist_name', 'tourist_email', 'tourist_phone', 'start_date', 'special_requests']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_start_date(self):
        import datetime
        data = self.cleaned_data['start_date']
        today = datetime.date.today()
        future_date = today + datetime.timedelta(days=3650)

        if data < today or data > future_date:
            raise forms.ValidationError("Start date must be within 10 years from today.")
        
        return data

class QueryForm(forms.ModelForm):
    class Meta:
        model=TripQueries
        fields=['name','phno','query']

class EditProfileForm(UserChangeForm):
    password = None  # Exclude the password field from the form

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_picture']