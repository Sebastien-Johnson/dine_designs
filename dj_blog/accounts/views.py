from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from .forms import CustomUserCreationForm, CustomUserChangeForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class EditProfileView(UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("post_list")
    template_name = "registration/edit_profile.html"

    def get_object(self):
        return self.request.user

class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm 
    success_url = reverse_lazy("password_success")

def password_success(request):
    return render(request, "registration/password_success.html", {})