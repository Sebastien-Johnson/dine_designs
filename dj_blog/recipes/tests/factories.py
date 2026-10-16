import factory
from datetime import timedelta
from django.utils import timezone
from accounts.models import CustomUser
from recipes.models import *


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Sequence(lambda n: f"chef_{n}")
    email = factory.LazyAttribute(
        lambda obj: f"{obj.username}@example.com"
    )
    password = factory.PostGenerationMethodCall(
        "set_password", "TestPassword123!"
    )


class FoodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Food

    name = factory.Faker("word")
    base_proteins = 20.0
    base_carbs = 10.0
    base_fats = 5.0
    base_calories = 165.0
    base_serving = 100.0
    base_unit = "g"


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

    title = factory.Faker("sentence", nb_words=4)
    #subfactories create dependencies for related models
    author = factory.SubFactory(UserFactory)
    published = factory.LazyFunction(
        timezone.localdate
    )
    cooking_time = timedelta(minutes=45)
    serves = 4


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient

    recipe = factory.SubFactory(RecipeFactory)
    food = factory.SubFactory(FoodFactory)
    serving_size = factory.LazyAttribute(
        lambda obj: obj.food.base_serving
    )
    serving_unit = factory.LazyAttribute(
        lambda obj: obj.food.base_unit
    )


class RatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rating

    recipe = factory.SubFactory(RecipeFactory)
    user = factory.SubFactory(UserFactory)
    score = 4


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    recipe = factory.SubFactory(RecipeFactory)
    name = factory.SubFactory(UserFactory)
    body = factory.Faker("paragraph")


class InstructionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Instruction

    
    recipe = factory.SubFactory(RecipeFactory)
    step_number = 1
    text = factory.Faker("sentence")