from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MealNameSuggestion(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class MealItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=255)
    portions_per_container = models.IntegerField()
    date_added = models.DateField()
    note = models.TextField(blank=True, null=True)
    date_consumed = models.DateField(blank=True, null=True, default=None)
    consumed_by_user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        related_name='consumed_meals', 
        blank=True, 
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.meal_name
