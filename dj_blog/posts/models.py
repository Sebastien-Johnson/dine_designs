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

    def get_author(self, request):
        self.author = request.user