from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Comment, Rating, Food
from .forms import CreateRecipe, AddComment, AddRating
from django.views.generic.list import ListView
from django.core import serializers
from django.conf import settings
import requests, json


class RecipeListView(ListView):
    model = Recipe
    template_name = "recipe_list.html"
    ordering = ["-published"]

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipe_detail.html"


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = CreateRecipe
    success_url = reverse_lazy("recipe_list")
    template_name = "recipe_create.html"
    context_object_name =  "recipe_data"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    def upload_file(self, request):
        if request.method == "POST":
            form = CreateRecipe(request.POST, request.DATA)
        
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect("recipe_list")
        else:
            form = CreateRecipe()
        return render(request, "recipe_create.html", {"form": form})

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

class FoodList(ListView):
    model = Food
    template_name = "partial/api_search_bar.html"
    context_object_name = "foods"

    def get_queryset(self):
        recipe = self.request.recipe
        return recipe.foods.all() 


def add_food(request):
    new_food = search_food(request)[0]

    request.foods.add(new_food)

    foods = request.form.foods.all()
    return render(request, "partials/food_list.html", {"foods": foods})

    #this is where to link to posts with model instance
    if request.POST.getlist("foods"):
        new_query = request.POST.copy()
        new_query.setlist("foods", new_food)
        request.POST = new_query
        foods = new_query.getlist("foods")
        return render(request, "partials/food_list.html", {"foods": foods})
    else:
        foods = request.POST.getlist("foods")
        foods.append(new_food)
        new_query = request.POST.copy()
        new_query.setlist("foods", foods)
        request.POST = new_query
        foods = request.POST.getlist("foods")
        return render(request, "partials/food_list.html", {"foods": foods})

def food_create_inline(request):
    if request.method == "POST":
        new_food = search_food(request)
        
        recipe_form = CreateRecipe(
            initial={
                "foods":[new_food.pk]
            }
        )
        print(recipe_form)
        
        return render(
            request,
            "partials/food_list.html",
            {
                "form": recipe_form,
                
            },
        )

   
    return render(
        request,
        "partials/api_search_bar.html",
    )

def search_food(request):
    key = str(settings.DJANGO_SECRET_KEY)
    #get user input 
    food_req = request.POST["foodname"]

    headers={"x-api-key":key}
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_req}"

    #pulls data from api
    response = requests.get(url, headers=headers)
    food_resp = response.json()["foods"]
    # get selected food json data from resp
    food_json = food_resp[0]
    new_food = create_food_item(food_json)

    return new_food[0]

def create_food_item(food_json):
    
    nutrients = food_json["foodNutrients"]
    macros = [
                ["protein", 1.0],
                ["carb", 1.0],
                ["fat", 1.0],
                ["energy", 1.0],
            ]
    
    for nutrient in nutrients:
        for macro in macros:
            if macro[0] in nutrient["nutrientName"].lower():
                macro[1] = nutrient["value"]
    
    new_food = Food.objects.get_or_create(
                            name=food_json["description"], 
                            proteins=float(macros[0][1]), 
                            carbs=float(macros[1][1]), 
                            fats=float(macros[2][1]), 
                            calories=float(macros[3][1]),  
                            base_serving=float(food_json["servingSize"]),
                            base_unit=food_json["servingSizeUnit"],
                        )
    
    
    return new_food

def delete_food(request, pk):
    request.foods.remove(pk)
    foods = request.foods.all()
    return render(request, "partials/food_list.html", {"foods": foods})

