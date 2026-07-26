from django import forms
from .models import Post

class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "author", "published", "cover", "description", "content")