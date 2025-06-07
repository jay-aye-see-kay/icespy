from django.contrib import admin
from .models import MealItem, MealNameSuggestion

# Register your models here.
admin.site.register(MealItem)
admin.site.register(MealNameSuggestion)
