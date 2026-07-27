from django import forms
from .models import Post

class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "author", "published", "cover", "description", "content")

        widgets = {
            'author': forms.TextInput(attrs={'class':'form-control', 'value':'', 'id':'author_name_field', 'type':'hidden'}),
        }