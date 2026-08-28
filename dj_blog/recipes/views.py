from django.views.generic import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Comment, Rating, Food
from .forms import CreateRecipe, AddComment, AddRating
from django.views.generic.list import ListView
from django.core import serializers
from django.conf import settings
import requests


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
    success_url = reverse_lazy("recipe_list")
    template_name = "recipe_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user

        response = super().form_valid(form)

        foods = self.request.POST.getlist("foods")
        food_ids = []
        for f in foods:
            if f:
                food_ids.append(int(f))

        self.object.foods.set(food_ids)

        return response

class RecipeEditView(UpdateView):
    model = Recipe
    form_class = CreateRecipe
    success_url = reverse_lazy("recipe_list")
    template_name = "recipe_edit.html"

    def edit_recipe(request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == "GET":
            context = {"form": CreateRecipe(instance=recipe), "pk": pk}
            return render(request,"post_edit.html", context)

        elif request.method == "POST":
            form = CreateRecipe(request.POST, instance=recipe)
            if form.is_valid():
                form.save()
                messages.success(request, "The recipe has been updated successfully.")
                return redirect("recipe_list")
            else:
                messages.error(request, "Please correct the following errors:")
                return render(request,"recipe_edit.html",{"form":form})

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
    foods = request.POST.getlist("foods")

    results = search_food(request)
    
    if not results:
        return HttpResponse("No food found")

    #gets or creates searched food
    food = create_food_item(results[0])

    #checks if food names in current form list
    if str(food.pk) not in foods:
        foods.append(str(food.pk))

    #filters selected foods from all food 
    food_ids = []
    for f in foods:
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


def search_food(request):
    key = str(settings.DJANGO_SECRET_KEY)
    #get user input 
    food_req = request.POST["foodname"]

    headers={"x-api-key":key}
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_req}"

    #pulls data from api
    response = requests.get(
        url, 
        headers=headers,
        params={"query": food_req},
        )
    
    response.raise_for_status()
    # get selected food json data from resp
    return response.json()["foods"]

def create_food_item(food_json):
    nutrients = food_json["foodNutrients"]
    
    protein = 0
    carbs = 0
    fat = 0
    calories = 0

    for nutrient in nutrients:
        name = nutrient["nutrientName"].lower()

        if "protein" in name:
            protein = nutrient["value"]

        elif "carbohydrate" in name:
            carbs = nutrient["value"]

        elif "fat" in name:
            fat = nutrient["value"]

        elif "energy" in name:
            calories = nutrient["value"]
    
    food, created = Food.objects.get_or_create(
        name=food_json["description"],
        defaults={
            "proteins": protein,
            "carbs": carbs,
            "fats": fat,
            "calories": calories,
            "base_serving": food_json.get("servingSize", 0),
            "base_unit": food_json.get("servingSizeUnit", ""),
        },
    )

    return food
