from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, EditProfileView, ChangePasswordView, password_success, ShowProfilePageView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("edit_profile/", EditProfileView.as_view(), name="edit_profile"),
    path("password/", ChangePasswordView.as_view(template_name="registration/change_password.html"), name="password"),
    path("password_success", password_success, name="password_success"),
    path("<int:pk>/profile/", ShowProfilePageView.as_view(), name="show_profile_page"),
]