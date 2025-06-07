from django.test import TestCase
from inventory.forms import AddMealForm # Assuming your form is in inventory.forms
from django.contrib.auth.models import User # If you need a User for testing
from inventory.models import MealItem, MealNameSuggestion # If needed for model interaction
import datetime
from django.utils import timezone
from datetime import timedelta

# Create your tests here.
class AddMealFormTest(TestCase):
    def test_form_invalid_missing_required_fields(self):
        """Test that the form is invalid if required fields are missing."""
        # Test with no data
        form = AddMealForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('meal_name', form.errors)
        self.assertIn('date_added', form.errors)
        self.assertIn('number_of_containers', form.errors)
        self.assertIn('portions_per_container', form.errors)

        # Test with some required fields missing
        form_data = {
            'meal_name': 'Test Meal',
            # date_added is missing
            'number_of_containers': 1,
            'portions_per_container': 1,
        }
        form = AddMealForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date_added', form.errors)
        self.assertNotIn('meal_name', form.errors) # meal_name is provided

    def test_form_valid_all_required_data(self):
        """Test that the form is valid when all required data is provided."""
        form_data = {
            'meal_name': 'Delicious Meal',
            'date_added': datetime.date.today(),
            'number_of_containers': 2,
            'portions_per_container': 3,
            'note': 'This is a test note.'
        }
        form = AddMealForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors.as_json()}")

    def test_form_invalid_negative_integers(self):
        """Test that the form is invalid if integer fields have values less than 1."""
        form_data = {
            'meal_name': 'Negative Test',
            'date_added': datetime.date.today(),
            'number_of_containers': 0, # Invalid
            'portions_per_container': -1, # Invalid
        }
        form = AddMealForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('number_of_containers', form.errors)
        self.assertIn('portions_per_container', form.errors)

    def test_form_note_is_optional(self):
        """Test that the note field is optional."""
        form_data = {
            'meal_name': 'No Note Meal',
            'date_added': datetime.date.today(),
            'number_of_containers': 1,
            'portions_per_container': 1,
            # 'note' is not provided
        }
        form = AddMealForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors.as_json()}")


class MealItemModelTest(TestCase):
    def setUp(self):
        # Create a user and a meal name suggestion for testing
        self.user = User.objects.create_user(username='testuser', password='password')
        self.meal_name_suggestion = MealNameSuggestion.objects.create(name='Test Soup')

    def test_age_property(self):
        # Test case 1: Added today
        meal_today = MealItem.objects.create(
            user=self.user,
            meal_name=self.meal_name_suggestion,
            portions_per_container=1,
            date_added=timezone.now().date()
        )
        self.assertEqual(meal_today.age, "Today")
        self.assertEqual(meal_today.age_in_days, 0)

        # Test case 2: Added 10 days ago
        ten_days_ago = timezone.now().date() - timedelta(days=10)
        meal_10_days = MealItem.objects.create(
            user=self.user,
            meal_name=self.meal_name_suggestion,
            portions_per_container=1,
            date_added=ten_days_ago
        )
        self.assertEqual(meal_10_days.age, "10 days")
        self.assertEqual(meal_10_days.age_in_days, 10)

        # Test case 3: Added 2 months and 5 days ago (approx 65 days)
        two_months_5_days_ago = timezone.now().date() - timedelta(days=65)
        meal_2_months_5_days = MealItem.objects.create(
            user=self.user,
            meal_name=self.meal_name_suggestion,
            portions_per_container=1,
            date_added=two_months_5_days_ago
        )
        # Note: The age property uses 30 days for a month for simplicity
        self.assertEqual(meal_2_months_5_days.age, "2 months, 5 days")
        self.assertEqual(meal_2_months_5_days.age_in_days, 65)

        # Test case 4: Added 1 year, 1 month, 1 day ago (approx 365 + 30 + 1 = 396 days)
        one_year_one_month_one_day_ago = timezone.now().date() - timedelta(days=396)
        meal_1_year_1_month_1_day = MealItem.objects.create(
            user=self.user,
            meal_name=self.meal_name_suggestion,
            portions_per_container=1,
            date_added=one_year_one_month_one_day_ago
        )
        self.assertEqual(meal_1_year_1_month_1_day.age, "1 year, 1 month, 1 day")
        self.assertEqual(meal_1_year_1_month_1_day.age_in_days, 396)

        # Test case 5: Consumed meal
        consumed_meal = MealItem.objects.create(
            user=self.user,
            meal_name=self.meal_name_suggestion,
            portions_per_container=1,
            date_added=timezone.now().date() - timedelta(days=5),
            date_consumed=timezone.now().date()
        )
        self.assertEqual(consumed_meal.age, "Consumed")
        self.assertEqual(consumed_meal.age_in_days, 0) # Or your desired value for consumed items

    def test_age_in_days_property(self):
        # Test case 1: Added today
        meal_today = MealItem.objects.create(
            user=self.user,
            meal_name=self.meal_name_suggestion,
            portions_per_container=1,
            date_added=timezone.now().date()
        )
        self.assertEqual(meal_today.age_in_days, 0)

        # Test case 2: Added 50 days ago
        fifty_days_ago = timezone.now().date() - timedelta(days=50)
        meal_50_days = MealItem.objects.create(
            user=self.user,
            meal_name=self.meal_name_suggestion,
            portions_per_container=1,
            date_added=fifty_days_ago
        )
        self.assertEqual(meal_50_days.age_in_days, 50)

        # Test case 3: Added 100 days ago
        hundred_days_ago = timezone.now().date() - timedelta(days=100)
        meal_100_days = MealItem.objects.create(
            user=self.user,
            meal_name=self.meal_name_suggestion,
            portions_per_container=1,
            date_added=hundred_days_ago
        )
        self.assertEqual(meal_100_days.age_in_days, 100)

        # Test case 4: Consumed meal
        consumed_meal_days_test = MealItem.objects.create(
            user=self.user,
            meal_name=self.meal_name_suggestion,
            portions_per_container=1,
            date_added=timezone.now().date() - timedelta(days=5),
            date_consumed=timezone.now().date()
        )
        self.assertEqual(consumed_meal_days_test.age_in_days, 0) # Assuming 0 for consumed items
