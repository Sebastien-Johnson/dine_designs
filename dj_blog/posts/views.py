from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import CreatePost



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
        if request.method == 'POST':
            form = CreatePost(request.POST, request.DATA)


    def upload_file(request):
        if request.method == 'POST':
            form = CreatePost(request.POST, request.DATA)

        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('post_list')
        else:
            form = CreatePost()
        return render(request, 'post_create.html', {'form': form})

class PostEditView(UpdateView):
    model = Post
    form_class = CreatePost
    success_url = reverse_lazy("post_list")
    template_name = "post_edit.html"

    def edit_post(request, pk):
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'GET':
            context = {'form': CreatePost(instance=post), 'pk': pk}
            return render(request,'post_edit.html', context)

        elif request.method == 'POST':
            form = CreatePost(request.POST, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'The post has been updated successfully.')
                return redirect('post_list')
            else:
                messages.error(request, 'Please correct the following errors:')
                return render(request,'post_edit.html',{'form':form})

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")
    template_name = "post_confirm_delete.html"

    def delete_post(request, id):
        post = get_object_or_404(Post, pk=id)
        context = {"post":post}

        if request.method == 'GET':
            return render(request, 'post_confirm_delete.html', context)
        elif request.method == 'POST':
            post.delete()
            messages.success(request, 'The post has been deleted successfully.')
            return redirect("post_list")