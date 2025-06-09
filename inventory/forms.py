from django import forms
from .models import MealItem

TAILWIND_FIELD_CLASSES = "w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"

class AddMealForm(forms.Form):
    meal_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': TAILWIND_FIELD_CLASSES
    }))
    date_added = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': TAILWIND_FIELD_CLASSES
    }))
    number_of_containers = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={
        'class': TAILWIND_FIELD_CLASSES
    }))
    portions_per_container = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={
        'class': TAILWIND_FIELD_CLASSES
    }))
    note = forms.CharField(widget=forms.Textarea(attrs={
        'class': TAILWIND_FIELD_CLASSES,
        'rows': 3
    }), required=False)

class EditMealForm(forms.ModelForm):
    class Meta:
        model = MealItem
        fields = ['meal_name', 'portions_per_container', 'date_added', 'note']
        widgets = {
            'meal_name': forms.TextInput(attrs={
                'class': TAILWIND_FIELD_CLASSES
            }),
            'portions_per_container': forms.NumberInput(attrs={
                'class': TAILWIND_FIELD_CLASSES
            }),
            'date_added': forms.DateInput(attrs={
                'type': 'date',
                'class': TAILWIND_FIELD_CLASSES
            }),
            'note': forms.Textarea(attrs={
                'class': TAILWIND_FIELD_CLASSES,
                'rows': 3
            }),
        }
