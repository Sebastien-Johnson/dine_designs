from unittest.mock import patch, Mock
from django.test import TestCase
from django.urls import reverse


class FoodSearchViewTests(TestCase):
    """Tests for searching the USDA FoodData Central API."""

    def setUp(self):
        self.url = reverse("search_food")

    @patch("recipes.views.requests.get")
    def test_search_returns_usda_food_results(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "foods": [
                {
                    "fdcId": 12345,
                    "description": "Chicken breast, raw",
                },
                {
                    "fdcId": 67890,
                    "description": "Chicken thigh, raw",
                },
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        response = self.client.get(
            self.url,
            {"foodname": "chicken"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "food_search_results.html"
        )
        self.assertContains(response, "Chicken breast, raw")
        self.assertContains(response, "Chicken thigh, raw")

        mock_get.assert_called_once()

    @patch("recipes.views.requests.get")
    def test_search_passes_query_to_usda_api(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"foods": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        self.client.get(self.url, {"foodname": "salmon"})

        _, kwargs = mock_get.call_args

        self.assertIn("params", kwargs)
        self.assertEqual(
            kwargs["params"]["query"], "salmon"
        )
        self.assertEqual(
            kwargs["params"]["pageSize"], 25
        )

    @patch("recipes.views.requests.get")
    def test_search_handles_no_results(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"foods": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        response = self.client.get(
            self.url,
            {"foodname": "foodthatdoesnotexist"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response, "Chicken breast, raw"
        )

    @patch("recipes.views.requests.get")
    def test_search_handles_api_failure(self, mock_get):
        mock_get.side_effect = Exception("API unavailable")

        response = self.client.get(
            self.url,
            {"foodname": "chicken"},
        )

        # This assumes your view catches API exceptions
        # and returns an error or empty-results fragment.
        self.assertEqual(response.status_code, 200)

    @patch("recipes.views.requests.get")
    def test_search_uses_expected_api_endpoint(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"foods": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        self.client.get(self.url, {"foodname": "chicken"})

        args, _ = mock_get.call_args

        self.assertEqual(
            args[0],
            "https://api.nal.usda.gov/fdc/v1/foods/search",
        )