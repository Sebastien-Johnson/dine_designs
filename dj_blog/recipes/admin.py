from django.contrib import admin
from .models import *

admin.site.register(Recipe, Comment, Rating, Food)