from django.urls import path
from .views import *

urlpatterns = [
    path("<int:pk>/", RecipeDetailView.as_view(), name="recipe_detail"),
    path("<int:pk>/recipe_edit/", RecipeEditView.as_view(), name="recipe_edit"),
    path("<int:pk>/recipe_confirm_delete/", RecipeDeleteView.as_view(), name="recipe_confirm_delete"),
    path("<int:pk>/recipe_rating/", RecipeRatingView.as_view(), name="recipe_rating"),
    path("<int:pk>/comment", AddCommentView.as_view(), name="add_comment"),
    
]

htmx_urlpatterns = [
    path("", RecipeListView.as_view(), name="recipe_list"),
    path("recipe_create/", RecipeCreateView.as_view(), name="recipe_create"),
    path("recipe_create/<int:food_id>/remove_food/", remove_food, name="remove_food"),
    path("add_food/", add_food, name="add_food"),
    path("search_food/", search_food, name="search_food"),
    path("recipe_create/<int:food_id>/calulate_food/", calculate_food, name="calculate_food")
]

urlpatterns += htmx_urlpatterns