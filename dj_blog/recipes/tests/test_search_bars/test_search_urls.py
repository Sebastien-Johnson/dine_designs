from django.test import SimpleTestCase
from django.urls import reverse, resolve
from recipes.views import search_food, recipe_search


class SearchURLTests(SimpleTestCase):
    def test_food_search_url_resolves(self):
        url = reverse("search_food")

        self.assertEqual(
            resolve(url).func,
            search_food,
        )

    def test_recipe_search_url_resolves(self):
        url = reverse("recipe_search")

        self.assertEqual(
            resolve(url).func,
            recipe_search,
        )