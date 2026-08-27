from django import forms
from .models import Recipe, Comment, Rating

class CreateRecipe(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ("title", "author", "published", "cover", "instructions", "foods")

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

