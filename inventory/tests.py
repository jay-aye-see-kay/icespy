from django.test import TestCase
from inventory.forms import AddMealForm # Assuming your form is in inventory.forms
from django.contrib.auth.models import User # If you need a User for testing
from inventory.models import MealItem, MealNameSuggestion # If needed for model interaction
import datetime

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
