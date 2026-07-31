from django import forms
from .models import Post, Comment

class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "author", "published", "cover", "description", "content")

        widgets = {
            'author': forms.TextInput(attrs={'class':'form-control', 'value':'', 'id':'author_name_field', 'type':'hidden'}),
        }


class AddComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)

        widgets = {
            #'name': forms.TextInput(attrs={"class": "form-control"}),
            'body': forms.Textarea(attrs={"class": "form-control"}),
        }
