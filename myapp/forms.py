from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Service, ServiceBooking

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    pet_name = forms.CharField(max_length=50)
    pet_type = forms.ChoiceField(choices=[('Dog', 'Dog'), ('Cat', 'Cat'), ('Other', 'Other')])
    pet_breed = forms.CharField(max_length=50)
    pet_age = forms.DecimalField(required=False, min_value=0.1, max_value=150)
    pet_gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')], required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password1', 'password2',
            'full_name', 'phone_number', 'address',
            'pet_name', 'pet_type', 'pet_breed', 'pet_age', 'pet_gender'
        ]

SLOT_CHOICES = [
    ('07:00 - 08:00', '07:00 - 08:00'),
    ('08:00 - 09:00', '08:00 - 09:00'),
    ('09:00 - 10:00', '09:00 - 10:00'),
    ('10:00 - 11:00', '10:00 - 11:00'),
    ('11:00 - 12:00', '11:00 - 12:00'),
    ('12:00 - 13:00', '12:00 - 13:00'),
    ('13:00 - 14:00', '13:00 - 14:00'),
    ('14:00 - 15:00', '14:00 - 15:00'),
    ('15:00 - 16:00', '15:00 - 16:00'),
    ('16:00 - 17:00', '16:00 - 17:00'),
    ('17:00 - 18:00', '17:00 - 18:00'),
    ('18:00 - 19:00', '18:00 - 19:00'),
]

class ServiceBookingForm(forms.ModelForm):
    preferred_slot = forms.ChoiceField(choices=SLOT_CHOICES, required=True)

    class Meta:
        model = ServiceBooking
        fields = ['service', 'preferred_slot']