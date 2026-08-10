from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Rating, Food
from .forms import CreatePost, AddComment, AddRating, CreateFood
from django.views.generic.list import ListView
import yaml, requests




class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    ordering = ["-published"]

class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"


class PostCreateView(CreateView):
    model = Post
    form_class = CreatePost
    success_url = reverse_lazy("post_list")
    template_name = "post_create.html"

    def add_author(request):
        if request.method == "POST":
            form = CreatePost(request.POST, request.DATA)


    def upload_file(request):
        if request.method == "POST":
            form = CreatePost(request.POST, request.DATA)

        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect("post_list")
        else:
            form = CreatePost()
        return render(request, "post_create.html", {"form": form})

class PostEditView(UpdateView):
    model = Post
    form_class = CreatePost
    success_url = reverse_lazy("post_list")
    template_name = "post_edit.html"

    def edit_post(request, pk):
        post = get_object_or_404(Post, pk=pk)

        if request.method == "GET":
            context = {"form": CreatePost(instance=post), "pk": pk}
            return render(request,"post_edit.html", context)

        elif request.method == "POST":
            form = CreatePost(request.POST, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, "The post has been updated successfully.")
                return redirect("post_list")
            else:
                messages.error(request, "Please correct the following errors:")
                return render(request,"post_edit.html",{"form":form})

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")
    template_name = "post_confirm_delete.html"

    def delete_post(request, id):
        post = get_object_or_404(Post, pk=id)
        context = {"post":post}

        if request.method == "GET":
            return render(request, "post_confirm_delete.html", context)
        elif request.method == "POST":
            post.delete()
            messages.success(request, "The post has been deleted successfully.")
            return redirect("post_list")

class AddCommentView(CreateView):
    model = Comment
    form_class = AddComment
    template_name = "add_comment.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        form.instance.post_id = self.kwargs["pk"]
        form.instance.name = self.request.user
        return super().form_valid(form)

class PostRatingView(CreateView):
    model = Rating
    form_class = AddRating
    template_name = "post_rating.html"
    success_url = reverse_lazy("post_list")

    #create rating and associate with post

    def form_valid(self, form):
        form.instance.post_id = self.kwargs["pk"]
        form.instance.user = self.request.user
        return super().form_valid(form)

class FoodList(ListView):
    model = Food
    template_name = "foods.html"
    context_object_name = "foods"

    def get_queryset(self):
        post = self.request.post 
        return post.ingredients.all()

def add_food(request):
    #with open("config.yaml", "r") as ymlfile:
        #cfg = yaml.safe_load(ymlfile)
        #key = str(cfg["usda_api_key"])
        #user's food query
    food_req = request.POST.get("food_name")
    headers={"x-api-key":"uFndqhD71Wkofc6ftcwEvlGyIfu4l0fS4yqAb7dC"}
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_req}"

    #user's food response
    response = requests.get(url, headers=headers)
    
    food_resp = response.json()["foods"]

    # get selected food json data from resp
    food_json = food_resp[0]

    new_food = create_food_item(food_json)

    #add new food to post creation view

    foods = request.food.all()
    return render(request, "partials/food_list.html", {"foods": foods})

def delete_food(request, pk):
    request.user.foods.remove(pk)
    foods = request.user.foods.all()
    return render(request, "partials/food_list.html", {"foods": foods})

def search_food(request):
    with open("config.yaml", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        key = str(cfg["usda_api_key"])
        #user's food query
        food_req = request.POST.get("search")
        headers={"x-api-key":key}
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_req}"
        results = requests.get(url, headers=headers)
        context = {"results":results}
        return render(request, "partials/search_results.html", context)
    


def create_food_item(food_json):
    nutrients = food_json["foodNutrients"]
    macros = [
                ["protien", 1.0],
                ["carb", 1.0],
                ["fat", 1.0],
                ["energy", 1.0],
            ]
    
    for nutrient in nutrients:
            for macro in macros:
                if macro[0].lower() in nutrient["nutrientName"].lower():
                    macro[1] = nutrient["value"]

    new_food = Food.objects.get_or_create(
                            name=food_json["description"], 
                            protiens=float(macros[0][1]), 
                            carbs=float(macros[1][1]), 
                            fats=float(macros[2][1]), 
                            calories=float(macros[3][1]),  
                            base_serving=float(food_json["servingSize"]),
                            base_unit=food_json["servingSizeUnit"],
                        )
    return new_food



class FoodCreateView(CreateView):
    model = Food
    form_class = CreateFood
    success_url = reverse_lazy("post_list")
    template_name = "food_create.html"

    def upload_file(request):
        if request.method == "POST":
            form = CreatePost(request.POST, request.DATA)

        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect("post_list")
        else:
            form = CreatePost()
        return render(request, "post_create.html", {"form": form})

