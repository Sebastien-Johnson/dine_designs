from django.views.generic import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Comment, Rating, Food, Ingredient
from .forms import CreateRecipe, AddComment, AddRating
from django.views.generic.list import ListView
from django.conf import settings
import requests, json


class RecipeListView(ListView):
    model = Recipe
    template_name = "recipe_list.html"
    ordering = ["-published"]

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipe_detail.html"

    def food_list(self, request):
        
        results = self.food_set
        if not results:
            return HttpResponse("No food found")

        #filters selected foods from all food 
        food_ids = []
        for f in results:
            if f:
                food_ids.append(int(f))
        selected_foods = Food.objects.filter(pk__in=food_ids)

        #returns foods as list items
        return render(
            request,
            "partials/food_list.html",
            {
                "foods": selected_foods,
            },
        )

class RecipeCreateView(CreateView):
    model = Recipe
    form_class = CreateRecipe
    template_name = "recipe_create.html"
    success_url = reverse_lazy("recipe_list")

    def form_valid(self, form):
        form.instance.author = self.request.user

        response = super().form_valid(form)

        food_ids = [
                food_id
                for food_id in self.request.POST.getlist("foods")
                if food_id
            ]

        for food_id in food_ids:
            food = Food.objects.get(pk=food_id)
            #gets final serving size from form
            serving_size = float(
                self.request.POST.get(
                    f"serving_size_{food_id}",
                    food.base_serving
                )
            )
            #creates new ingredient obj from serving size
            Ingredient.objects.create(
                recipe=self.object,
                food=food,
                serving_size=serving_size,
                serving_unit=food.base_unit,
            )

        return response

class RecipeEditView(UpdateView):
    model = Recipe
    form_class = CreateRecipe
    success_url = reverse_lazy("recipe_list")
    template_name = "recipe_edit.html"

    def form_valid(self, form):
        # Save title, instructions, cover, etc.
        response = super().form_valid(form)

        # Get the foods submitted by the hidden inputs
        food_ids = [
            food_id
            for food_id in self.request.POST.getlist("foods")
            if food_id
        ]

         # Remove ingredients that are no longer in the recipe
        Ingredient.objects.filter(
            recipe=self.object
        ).exclude(
            food_id__in=food_ids
        ).delete()

        # Create/update each ingredient
        for food_id in food_ids:
            food = get_object_or_404(Food, pk=food_id)

            serving_size = float(
                self.request.POST.get(
                    f"serving_size_{food_id}",
                    food.base_serving
                )
            )

            Ingredient.objects.update_or_create(
                recipe=self.object,
                food=food,
                defaults={
                    "serving_size": serving_size,
                    "serving_unit": food.base_unit,
                },
            )

        messages.success(
            self.request,
            "The recipe has been updated successfully."
        )

        return response

class RecipeDeleteView(DeleteView):
    model = Recipe
    success_url = reverse_lazy("recipe_list")
    template_name = "recipe_confirm_delete.html"

    def delete_recipe(request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        context = {recipe}

        if request.method == "GET":
            return render(request, "recipe_confirm_delete.html", context)
        elif request.method == "POST":
            recipe.delete()
            messages.success(request, "The recipe has been deleted successfully.")
            return redirect("recipe_list")

class AddCommentView(CreateView):
    model = Comment
    form_class = AddComment
    template_name = "add_comment.html"
    success_url = reverse_lazy("recipe_list")

    def form_valid(self, form):
        form.instance.post_id = self.kwargs["pk"]
        form.instance.name = self.request.user
        return super().form_valid(form)

class RecipeRatingView(CreateView):
    model = Rating
    form_class = AddRating
    template_name = "recipe_rating.html"
    success_url = reverse_lazy("recipe_list")

    #create rating and associate with post

    def form_valid(self, form):
        form.instance.recipe_id = self.kwargs["pk"]
        form.instance.user = self.request.user
        return super().form_valid(form)

def add_food(request):
    """ gets or creates food for recipe creation form """
    fdc_id = request.POST.get("fdc_id")

    if not fdc_id:
        return HttpResponseBadRequest("No food selected.")
    #retrieves single food via fdc_id
    url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}"

    params = {
        "api_key": settings.USDA_API_KEY,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    food_json = response.json()

    #gets or creates searched food
    food = create_food_item(food_json)

    #gets existing list of form's foods
    food_ids = [
        food_id
        for food_id in request.POST.getlist("foods")
        if food_id
    ]

    #checks if food names in current form list
    if str(food.pk) not in food_ids:
        food_ids.append(str(food.pk))

    #filters selected foods from all food
    foods = Food.objects.filter(pk__in=food_ids)

    #returns foods as list items
    return render(
        request,
        "partials/food_list.html",
        {
            "foods": foods,
        },
    )


def search_food(request):
    """ gets list of foods for drop down menu """
    food_req = request.GET.get("foodname", "").strip()

    if not food_req:
        return render(
            request,
            "partials/food_search_results.html",
            {"foods": []},
        )
    # retrieves list of foods via name (description)
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "api_key": settings.USDA_API_KEY,
        "query": food_req,
        "pageSize": 25,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    results = response.json().get("foods", [])

    return render(
        request,
        "partials/food_search_results.html",
        {"foods": results},
    )

def create_food_item(food_json):
    """ gets or creates food item """
    foodNutrients = food_json.get("foodNutrients", [])

    

    proteins = 0
    carbs = 0
    fats = 0
    calories = 0

    for nutrient in foodNutrients:
        name = nutrient["nutrient"]["name"]

        if "Protein" in name:
            proteins = nutrient["amount"]

        elif "Carbohydrate, by difference" in name:
            carbs = nutrient["amount"]

        elif "Total lipid (fat)" in name:
            fats = nutrient["amount"]

        elif "Energy" in name:
            calories = nutrient["amount"]

    name = ""
    if "brandName" in food_json:
        name = (food_json["description"]+", "+food_json["brandName"]).title()
    else:
        name=(food_json["description"]).title()

    
    food, created = Food.objects.get_or_create(
        name=name,
        defaults={
            "base_proteins": proteins,
            "base_carbs": carbs,
            "base_fats": fats,
            "base_calories": calories,
            "base_serving": food_json.get("servingSize", 100),
            "base_unit": food_json.get("servingSizeUnit", "g"),
        },
    )

    return food

def calculate_food(request, food_id):
    food = get_object_or_404(Food, pk=food_id)

    serving_size = float(
        request.POST.get(f"serving_size_{food_id}", food.base_serving)
    )

    multiplier = serving_size / food.base_serving

    proteins = round((food.base_proteins * multiplier), 1)
    carbs = round((food.base_carbs * multiplier), 1)
    fats = round((food.base_fats * multiplier), 1)
    calories = round((proteins * 4 + carbs * 4 + fats * 9), 1)

    return render(
        request,
        "partials/food_nutrition.html",
        {
            "proteins": proteins,
            "carbs": carbs,
            "fats": fats,
            "calories": calories,
        },
    )

def remove_food(request, food_id):
    """Removes food from creation form, maintains obj in db """
    return HttpResponse("")


def add_food_edit(request, recipe_id):
    """Add a food to an existing recipe while preserving
    the current serving sizes in the edit form.
    """
    print(f"test: {request.POST.items()}")
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    fdc_id = request.POST.get("fdc_id")

    if not fdc_id:
        return HttpResponseBadRequest("No food selected.")

    # Get food from USDA
    url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}"

    params = {
        "api_key": settings.USDA_API_KEY,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    food_json = response.json()

    # Get or create the Food object
    food = create_food_item(food_json)

    # ---------------------------------------------------------
    # Preserve the serving sizes currently displayed in the form
    # ---------------------------------------------------------
    #check what django recieves
    for key, value in request.POST.items():

        if key.startswith("serving_size_"):
            food_id = key.replace("serving_size_", "")

            try:
                food_id = int(food_id)
                serving_size = float(value)
            except (ValueError, TypeError):
                continue

            # Find the existing ingredient
            ingredient = Ingredient.objects.filter(
                recipe=recipe,
                food_id=food_id
            ).first()

            if ingredient:
                ingredient.serving_size = serving_size
                ingredient.serving_unit = ingredient.food.base_unit
                ingredient.save()

    # ---------------------------------------------------------
    # Add the newly selected food
    # ---------------------------------------------------------

    Ingredient.objects.get_or_create(
        recipe=recipe,
        food=food,
        defaults={
            "serving_size": food.base_serving,
            "serving_unit": food.base_unit,
        },
    )

    # Get the complete ingredient list AFTER adding the new food
    ingredients = recipe.ingredients.select_related("food").all()

    return render(
        request,
        "partials/food_list_edit.html",
        {
            "recipe": recipe,
            "ingredients": ingredients,
        },
    )

def search_food_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    food_req = request.GET.get("foodname", "").strip()

    if not food_req:
        return render(
            request,
            "partials/food_search_results_edit.html",
            {
                "foods": [],
                "recipe": recipe,
            },
        )

    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "api_key": settings.USDA_API_KEY,
        "query": food_req,
        "pageSize": 25,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    results = response.json().get("foods", [])

    return render(
        request,
        "partials/food_search_results_edit.html",
        {
            "foods": results,
            "recipe": recipe,
        },
    )