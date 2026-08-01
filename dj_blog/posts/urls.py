from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post_create/", PostCreateView.as_view(), name="post_create"),
    path("<int:pk>/post_edit/", PostEditView.as_view(), name="post_edit"),
    path("<int:pk>/post_confirm_delete/", PostDeleteView.as_view(), name="post_confirm_delete"),
    path("<int:pk>/post_rating/", PostRatingView.as_view(), name="post_rating"),
    path("<int:pk>/post_edit_rating/", PostEditRatingView.as_view(), name="post_edit_rating"),
    path("", PostListView.as_view(), name="post_list"),
    path("<int:pk>/comment", AddCommentView.as_view(), name="add_comment"),
]