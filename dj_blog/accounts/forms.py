from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser, Profile

class CustomUserCreationForm(AdminUserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")

class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = CustomUser
        fields = ("username", "email")

class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "profile_pic", "website_url", "bookface_url", "litter_url", "denturest_url", "delaypound_url")

        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control"}),
            "website_url": forms.TextInput(attrs={"class": "form-control"}),
            "bookface_urk": forms.TextInput(attrs={"class": "form-control"}),
            "litter_url": forms.TextInput(attrs={"class": "form-control"}),
            "denturest_url": forms.TextInput(attrs={"class": "form-control"}), 
            "delaypound_url": forms.TextInput(attrs={"class": "form-control"}),
        }