from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass
    #pass

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(upload_to="images/profile/", blank=True, null=True)
    website_url = models.CharField(max_length=255, null=True, blank=True)
    bookface_url = models.CharField(max_length=255, null=True, blank=True)
    litter_url = models.CharField(max_length=255, null=True, blank=True)
    denturest_url = models.CharField(max_length=255, null=True, blank=True)
    delaypound_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("post_list")