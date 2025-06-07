from django import forms
from .models import MealItem  # Ensure you import the MealItem model

class AddMealForm(forms.Form):
    meal_name = forms.CharField()
    date_added = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    number_of_containers = forms.IntegerField(min_value=1)
    portions_per_container = forms.IntegerField(min_value=1)
    note = forms.CharField(widget=forms.Textarea, required=False)

class EditMealForm(forms.ModelForm):
    class Meta:
        model = MealItem
        fields = ['meal_name', 'portions_per_container', 'date_added', 'note']
        widgets = {
            'meal_name': forms.TextInput(attrs={
                'list': 'meal-name-suggestions-list' # Add datalist attribute for existing EditMealForm
            }),
            'date_added': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }
