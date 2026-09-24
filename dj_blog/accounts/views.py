from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView, LogoutView
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfilePageForm
from .models import Profile, CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class EditAccountView(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("recipe_list")
    template_name = "registration/edit_account.html"

    def get_object(self):
        return self.request.user

class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm 
    template_name = "registration/edit_profile_page.html"
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
    
class EditProfilePageView(UpdateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = "registration/edit_profile_page.html"
    success_url = reverse_lazy("recipe_list")
    
    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "password_form" not in context:
            context["password_form"] = PasswordChangeForm(
                user=self.request.user
            )

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Determine which form was submitted
        if "change_password" in request.POST:
            password_form = PasswordChangeForm(
                user=request.user,
                data=request.POST
            )

            if password_form.is_valid():
                password_form.save()

                return redirect("password_success")

            context = self.get_context_data()
            context["password_form"] = password_form

            return self.render_to_response(context)

        # Otherwise process the profile form
        return super().post(request, *args, **kwargs)

class CustomLogoutView(LogoutView):
    next_page = "recipe_list"