from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post_create/", PostCreateView.as_view(), name="post_create"),
    path('post_edit/<int:id>/', views.edit_post, name='post_edit'),
    path("", PostListView.as_view(), name="post_list"),
]