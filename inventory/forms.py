from django import forms
from .models import MealItem

BOOTSTRAP_FIELD_CLASSES = "form-control"

class AddMealForm(forms.Form):
    meal_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': BOOTSTRAP_FIELD_CLASSES,
        'placeholder': 'Enter meal name'
    }))
    date_added = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': BOOTSTRAP_FIELD_CLASSES
    }))
    number_of_containers = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={
        'class': BOOTSTRAP_FIELD_CLASSES,
        'placeholder': 'Number of containers'
    }))
    portions_per_container = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={
        'class': BOOTSTRAP_FIELD_CLASSES,
        'placeholder': 'Portions per container'
    }))
    note = forms.CharField(widget=forms.Textarea(attrs={
        'class': BOOTSTRAP_FIELD_CLASSES,
        'rows': 3,
        'placeholder': 'Optional notes'
    }), required=False)

class EditMealForm(forms.ModelForm):
    class Meta:
        model = MealItem
        fields = ['meal_name', 'portions_per_container', 'date_added', 'note']
        widgets = {
            'meal_name': forms.TextInput(attrs={
                'class': BOOTSTRAP_FIELD_CLASSES
            }),
            'portions_per_container': forms.NumberInput(attrs={
                'class': BOOTSTRAP_FIELD_CLASSES
            }),
            'date_added': forms.DateInput(attrs={
                'type': 'date',
                'class': BOOTSTRAP_FIELD_CLASSES
            }),
            'note': forms.Textarea(attrs={
                'class': BOOTSTRAP_FIELD_CLASSES,
                'rows': 3
            }),
        }
