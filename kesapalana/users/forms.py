from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, UserProfile, Address

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='Bio')
    location = forms.CharField(max_length=100, required=False, label='Location')
    website = forms.URLField(required=False, label='Website')
    class Meta:
        model = UserProfile
        fields = ('phone', 'avatar', 'date_of_birth', 'bio', 'location', 'website')

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('full_name', 'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country', 'phone', 'is_default')
