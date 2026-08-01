from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Rating
from .forms import CreatePost, AddComment, AddRating



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

class PostEditRatingView(UpdateView):
    model = Rating
    form_class = AddRating
    template_name = "post_edit_rating.html"
    success_url = reverse_lazy("post_list")

    def edit_post_rating(request, pk):
        rating = get_object_or_404(Rating, pk=pk)
        if request.method == "GET":
            context = {"form": AddRating(instance=rating), "pk": pk}
            return render(request,"post_edit_rating.html", context)

        elif request.method == "POST":
            form = AddRating(request.Rating, instance=rating)
            if form.is_valid():
                form.save()
                messages.success(request, "The rating has been updated successfully.")
                return redirect("post_list")
            else:
                messages.error(request, "Please correct the following errors:")
                return render(request,"post_edit_rating.html",{"form":form})