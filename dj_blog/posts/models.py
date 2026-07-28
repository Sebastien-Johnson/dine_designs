from django.db import models
from datetime import datetime
from accounts.models import CustomUser 


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    cover = models.ImageField(upload_to="images/", blank=True, null=True)
    description = models.CharField(max_length=100)
    content = models.TextField()
    published = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title + " | " + str(self.author)

# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, related_name="comments")
#     name = user.name
#     body = models.TextField()
#     created_on = models.DateTimeField(auto_now_add=True)
#     active = models.BooleanField(default=False)

#     class Meta:
#         ordering = ["created_on"]

#     def __str__(self):
#         return f"{self.post.title} by {self.name}" 