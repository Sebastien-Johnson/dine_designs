from django.urls import path
from .views import *

urlpatterns = [
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post_create/", PostCreateView.as_view(), name="post_create"),
    path("<int:pk>/post_edit/", PostEditView.as_view(), name="post_edit"),
    path("<int:pk>/post_confirm_delete/", PostDeleteView.as_view(), name="post_confirm_delete"),
    path("<int:pk>/post_rating/", PostRatingView.as_view(), name="post_rating"),
    path("<int:pk>/comment", AddCommentView.as_view(), name="add_comment"),
    path("foods/", FoodList.as_view(), name="food_list"),
    path("", PostListView.as_view(), name="post_list"),
]

htmx_urlpatterns = [
    path("add_food/", add_food, name="add_food")
]

urlpatterns += htmx_urlpatterns