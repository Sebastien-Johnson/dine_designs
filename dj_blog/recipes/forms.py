from django import forms
from .models import Recipe, Comment, Rating

class CreateRecipe(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ("title", "published", "cover", "instructions")


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

