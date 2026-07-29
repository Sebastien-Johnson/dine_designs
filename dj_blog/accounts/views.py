from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Profile


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

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = "registration/user_profile.html"

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)

        page_user = get_object_or_404(Profile, id=self.kwargs["pk"])

        context["page_user"] = page_user
        return context