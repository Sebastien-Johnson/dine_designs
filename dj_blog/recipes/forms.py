from django import forms
from .models import Recipe, Comment, Rating

class CreateRecipe(forms.ModelForm):
    cooking_hours = forms.IntegerField(
        required=False,
        min_value=0,
        label="Hours"
    )

    cooking_minutes = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=59,
        label="Minutes"
    )
    class Meta:
        model = Recipe
        fields = ("title", "published", "cover", "serves")


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
            "score": forms.NumberInput(attrs={'class': 'form-control', "min":0, "max":5}),
        }

