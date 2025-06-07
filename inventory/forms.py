from django import forms

class AddMealForm(forms.Form):
    meal_name = forms.CharField()
    date_added = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    number_of_containers = forms.IntegerField(min_value=1)
    portions_per_container = forms.IntegerField(min_value=1)
    note = forms.CharField(widget=forms.Textarea, required=False)
