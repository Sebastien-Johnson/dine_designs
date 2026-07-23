from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView

urlpatterns = [
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post_create/", PostCreateView.as_view(), name="post_create"),
    path("", PostListView.as_view(), name="post_list"),
]