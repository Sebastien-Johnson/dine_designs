from django.db import models
from datetime import datetime
from django.db.models import Avg
from accounts.models import CustomUser 
from django.core.validators import MaxValueValidator, MinValueValidator
from django.http import request


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(CustomUser, related_name="posts", on_delete=models.CASCADE, default=None)
    cover = models.ImageField(upload_to="images/", blank=True, null=True)
    ingredients = models.TextField(max_length=200)
    instructions = models.TextField()
    published = models.DateTimeField(default=f"{datetime.today().day}/{datetime.today().month}/{datetime.today().year}")
    ratings = models.ManyToManyField(CustomUser, through="Rating", through_fields=("post", "user"))
    

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