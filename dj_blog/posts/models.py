from django.db import models
from datetime import date
from django.db.models import Avg
from accounts.models import CustomUser 

#access food via food_set
class IngredientList(models.Model):
    proteins = 0
    carbs = 0
    fats = 0
    calories = 0

    def compile_macros(self):
        for food in self.foods:
            self.proteins += food.proteins
            self.carbs += food.carbs
            self.fats += food.fats
            self.calories += food.calories

    def __str__(self):
        return f"{self.posts}, {self.foods}"

class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(CustomUser, related_name="posts", on_delete=models.CASCADE, default=None)
    cover = models.ImageField(upload_to="images/", blank=True, null=True)
    instructions = models.TextField()
    published = models.DateField(default=(f"{date.today().month}/{date.today().day}/{date.today().year}"))
    ratings = models.ManyToManyField(CustomUser, through="Rating", through_fields=("post", "user"))
    proteins = models.IntegerField(default=0)
    carbs = models.IntegerField(default=0)
    fats = models.IntegerField(default=0)
    calories = models.IntegerField(default=0)
    ingredient_list = models.OneToOneField(IngredientList, default=None, on_delete=models.RESTRICT, related_name="posts")
    
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
        return Rating.objects.filter(post=self).aggregate(Avg("score"))["score__avg"] or 0

    def get_review_count(self):
        return len(self.get_all_reviewers())

    # def compile_macros(self):
    #     for ingredientList in self.ingredientList:
    #         self.proteins += ingredientList.proteins
    #         self.carbs += ingredientList.carbs
    #         self.fats += ingredientList.fats
    #         self.calories += ingredientList.calories


class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.post.title}: {self.score}"

    class Meta:
        unique_together = ('post','user')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, related_name="comments")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"{self.post.title} by {self.name}"


class Food(models.Model):
    name = models.CharField(max_length=200)
    protiens = models.IntegerField()
    carbs = models.IntegerField()
    fats = models.IntegerField()
    calories = models.IntegerField()
    base_serving = models.IntegerField() 
    base_unit = models.CharField()
    ingredient_list = models.ForeignKey(IngredientList, default=None, on_delete=models.RESTRICT, related_name="foods")