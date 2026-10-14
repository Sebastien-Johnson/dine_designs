
from datetime import timedelta

from django.test import TestCase

from recipes.models import (
    Food,
    Ingredient,
    Instruction,
    Rating,
    Recipe,
)
from recipes.tests.factories import (
    UserFactory,
    FoodFactory,
    RecipeFactory,
    IngredientFactory,
    RatingFactory,
    CommentFactory,
    InstructionFactory,
)


class FoodModelTests(TestCase):
    def test_food_factory_creates_food(self):
        food = FoodFactory(name="Chicken")

        self.assertEqual(food.name, "Chicken")
        self.assertEqual(food.base_serving, 100.0)

    def test_food_default_nutrition_values(self):
        food = Food.objects.create(name="Water")

        self.assertEqual(food.base_proteins, 0)
        self.assertEqual(food.base_calories, 0)


class RecipeModelTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.recipe = RecipeFactory(
            author=self.user,
            title="Chicken Rice",
            serves=4,
        )

    def test_recipe_string_representation(self):
        self.assertIn("Chicken Rice", str(self.recipe))
        self.assertIn(self.user.username, str(self.recipe))

    def test_recipe_defaults(self):
        recipe = Recipe.objects.create(author=self.user)

        self.assertEqual(recipe.title, "")
        self.assertEqual(recipe.serves, 1)
        self.assertEqual(recipe.average_rating(), 0)

    def test_average_rating(self):
        other_user = UserFactory()

        RatingFactory(
            recipe=self.recipe,
            user=self.user,
            score=4,
        )
        RatingFactory(
            recipe=self.recipe,
            user=other_user,
            score=2,
        )

        self.assertEqual(self.recipe.average_rating(), 3.0)

    def test_review_count(self):
        RatingFactory(recipe=self.recipe, user=self.user)
        RatingFactory(
            recipe=self.recipe,
            user=UserFactory(),
            score=5,
        )

        self.assertEqual(self.recipe.get_review_count(), 2)

    def test_get_user_rating(self):
        rating = RatingFactory(
            recipe=self.recipe,
            user=self.user,
            score=5,
        )

        self.assertEqual(
            self.recipe.get_user_rating(self.user),
            rating,
        )

    def test_get_user_rating_when_none_exists(self):
        self.assertIsNone(
            self.recipe.get_user_rating(self.user)
        )

    def test_cooking_time_display(self):
        self.recipe.cooking_time = timedelta(
            hours=1, minutes=30
        )

        self.assertEqual(
            self.recipe.cooking_time_display,
            "1 hour 30 minutes",
        )

    def test_cooking_time_display_for_minutes_only(self):
        self.recipe.cooking_time = timedelta(minutes=45)

        self.assertEqual(
            self.recipe.cooking_time_display,
            "45 minutes",
        )

    def test_cooking_time_display_when_empty(self):
        self.recipe.cooking_time = None

        self.assertEqual(
            self.recipe.cooking_time_display,
            "",
        )


class IngredientModelTests(TestCase):
    def setUp(self):
        self.recipe = RecipeFactory()
        self.food = FoodFactory(
            base_proteins=20,
            base_carbs=10,
            base_fats=5,
            base_calories=165,
            base_serving=100,
            base_unit="g",
        )

    def test_ingredient_multiplier(self):
        ingredient = IngredientFactory(
            recipe=self.recipe,
            food=self.food,
            serving_size=200,
        )

        self.assertEqual(ingredient.multiplier, 2)

    def test_ingredient_nutrition_values(self):
        ingredient = IngredientFactory(
            recipe=self.recipe,
            food=self.food,
            serving_size=200,
        )

        self.assertEqual(ingredient.proteins, 40)
        self.assertEqual(ingredient.carbs, 20)
        self.assertEqual(ingredient.fats, 10)
        self.assertEqual(ingredient.calories, 330)

    def test_recipe_total_macros(self):
        IngredientFactory(
            recipe=self.recipe,
            food=self.food,
            serving_size=200,
        )
        second_food = FoodFactory(
            base_proteins=10,
            base_carbs=20,
            base_fats=2,
            base_calories=150,
            base_serving=100,
        )
        IngredientFactory(
            recipe=self.recipe,
            food=second_food,
            serving_size=100,
        )

        self.assertEqual(self.recipe.total_proteins, 50)
        self.assertEqual(self.recipe.total_carbs, 40)
        self.assertEqual(self.recipe.total_fats, 12)
        self.assertEqual(self.recipe.total_calories, 480)

    def test_per_serving_nutrition(self):
        IngredientFactory(
            recipe=self.recipe,
            food=self.food,
            serving_size=200,
        )

        self.recipe.serves = 4

        self.assertEqual(self.recipe.calories_per_serving, 82.5)
        self.assertEqual(self.recipe.proteins_per_serving, 10.0)


class RatingModelTests(TestCase):
    def test_rating_string_representation(self):
        rating = RatingFactory(score=5)

        self.assertEqual(
            str(rating),
            f"{rating.recipe.title}: 5",
        )

    def test_user_cannot_rate_recipe_twice(self):
        from django.db import IntegrityError, transaction

        rating = RatingFactory(score=3)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Rating.objects.create(
                    recipe=rating.recipe,
                    user=rating.user,
                    score=5,
                )


class CommentAndInstructionModelTests(TestCase):
    def test_comment_string_representation(self):
        comment = CommentFactory()

        self.assertEqual(
            str(comment),
            f"{comment.recipe.title} by {comment.name}",
        )

    def test_comments_are_ordered_by_creation(self):
        recipe = RecipeFactory()
        first = CommentFactory(recipe=recipe)
        second = CommentFactory(recipe=recipe)

        comments = list(recipe.comments.all())

        self.assertEqual(comments, [first, second])

    def test_instruction_string_representation(self):
        instruction = InstructionFactory(
            step_number=2,
            text="Chop vegetables",
        )

        self.assertEqual(
            str(instruction),
            f"{instruction.recipe.title} - Step 2",
        )

    def test_deleting_recipe_deletes_ingredients_instructions_and_ratings(self):
        recipe = RecipeFactory()
        ingredient = IngredientFactory(recipe=recipe)
        instruction = InstructionFactory(recipe=recipe)
        rating = RatingFactory(recipe=recipe)

        ingredient_id = ingredient.pk
        instruction_id = instruction.pk
        rating_id = rating.pk

        recipe.delete()

        self.assertFalse(
            Ingredient.objects.filter(pk=ingredient_id).exists()
        )
        self.assertFalse(
            Instruction.objects.filter(pk=instruction_id).exists()
        )
        self.assertFalse(
            Rating.objects.filter(pk=rating_id).exists()
        )