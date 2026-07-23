from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to="images/", blank=True, null=True)
    description = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title