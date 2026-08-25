from django.urls import path
from .views import *

urlpatterns = [
    path("<int:pk>/", RecipeDetailView.as_view(), name="recipe_detail"),
    path("recipe_create/", RecipeCreateView.as_view(), name="recipe_create"),
    path("<int:pk>/recipe_edit/", RecipeEditView.as_view(), name="recipe_edit"),
    path("<int:pk>/recipe_confirm_delete/", RecipeDeleteView.as_view(), name="recipe_confirm_delete"),
    path("<int:pk>/recipe_rating/", RecipeRatingView.as_view(), name="recipe_rating"),
    path("<int:pk>/comment", AddCommentView.as_view(), name="add_comment"),
    path("foods/", FoodList.as_view(), name="food_list"),
    path("", RecipeListView.as_view(), name="recipe_list"),
]

htmx_urlpatterns = [
    path("add_food/", add_food, name="add_food"),
    path("delete_food/<int:pk>", delete_food, name="delete_food"),
    path("search_food/", search_food, name="search_food"),
]

urlpatterns += htmx_urlpatterns