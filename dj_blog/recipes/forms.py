from django import forms
from django.forms import formset_factory
from .models import Recipe, Comment, Rating, Food

class CreateRecipe(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ("title", "author", "published", "cover", "instructions", "foods")

        widgets = {
            "author": forms.TextInput(attrs={"class":"form-control", "value":"", "id":"author_name_field", "type":"hidden"}),
            "foods": forms.TextInput(attrs={"type":"hidden"})
        }

class CreateFood(forms.ModelForm):
    class Meta:
        model = Food
        fields = []

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

