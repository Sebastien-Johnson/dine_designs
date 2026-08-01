from django import forms
from .models import Post, Comment, Rating
class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "author", "published", "cover", "ingredients", "instructions" )

        widgets = {
            "author": forms.TextInput(attrs={"class":"form-control", "value":"", "id":"author_name_field", "type":"hidden"}),
        }


class AddComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)

        widgets = {
            "body": forms.Textarea(attrs={"class": "form-control"}),
        }

class AddRating(forms.ModelForm):
     class Meta:
        model = Rating
        fields = ("score",)

        widgets = {
            "score": forms.NumberInput(attrs={'class': 'form-control'}),
        }
