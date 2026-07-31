from django.urls import path
from .views import SignUpView, EditAccountView, ChangePasswordView, password_success, ShowProfilePageView, EditProfilePageView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("edit_profile/", EditAccountView.as_view(), name="edit_account"),
    path("password/", ChangePasswordView.as_view(template_name="registration/change_password.html"), name="password"),
    path("password_success", password_success, name="password_success"),
    path("<int:pk>/profile/", ShowProfilePageView.as_view(), name="show_profile_page"),
    path("<int:pk>/edit_profile_page/", EditProfilePageView.as_view(), name="edit_profile_page"),
]