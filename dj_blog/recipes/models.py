from django.db import models
from datetime import date
from django.db.models import Avg
from accounts.models import CustomUser 

#author
class Food(models.Model):
    name = models.CharField(max_length=200)
    proteins = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fats = models.FloatField(default=0)
    calories = models.FloatField(default=0)
    base_serving = models.FloatField(default=0) 
    base_unit = models.CharField(max_length=10, default="")

class RecipeManager(models.Manager):
    def create_recipe(self, request):
        recipe = self.create(author=request.user)
        return recipe
#book
class Recipe(models.Model):
    title = models.CharField(max_length=100, default="")
    author = models.ForeignKey(CustomUser, related_name="recipes", on_delete=models.CASCADE, default=None)
    cover = models.ImageField(upload_to="images/", blank=True, null=True)
    instructions = models.TextField(default="")
    published = models.DateField(default=(f"{date.today().year}-{date.today().month}-{date.today().day}"))
    ratings = models.ManyToManyField(CustomUser, through="Rating", through_fields=("recipe", "user"))
    proteins = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fats = models.FloatField(default=0)
    calories = models.FloatField(default=0)
    objects = RecipeManager()
    foods = models.ManyToManyField(Food)
    

    def __str__(self):
        return f"{self.title}, by {str(self.author)} ({self.average_rating()}/5★)"

    def match_reviewer(self):
        return self.get_all_reviewers()
    
    def get_all_reviewers(self):
        reviewers = []
        for rating in self.ratings.all():
            reviewers.append(rating)
        return reviewers

    def get_rating(self):
        return self.average_rating()

    def average_rating(self):
        return Rating.objects.filter(recipe=self).aggregate(Avg("score"))["score__avg"] or 0

    def get_review_count(self):
        return len(self.get_all_reviewers())

    def compile_macros(self):
        for food in self.foods:
            self.proteins += food.proteins
            self.carbs += food.carbs
            self.fats += food.fats
            self.calories += food.calories

class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.recipe.title}: {self.score}"

    class Meta:
        unique_together = ('recipe','user')

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")
    name = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, related_name="comments")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"{self.recipe.title} by {self.name}"



    