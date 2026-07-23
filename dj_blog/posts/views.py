from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Post
from .forms import CreatePost


class PostListView(ListView):
    model = Post
    template_name = "post_list.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"

class PostCreateView(CreateView):
    model = Post
    form_class = CreatePost
    success_url = reverse_lazy("post_list")
    template_name = "post_create.html"

    def upload_file(request):
        if request.method == 'POST':
            form = CreatePost(request.POST, request.DATA)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('post_list')
        else:
            form = CreatePost()
        return render(request, 'upload.html', {'form': form})