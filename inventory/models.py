from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class MealItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=255)  # Changed from ForeignKey to CharField
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

    @property
    def age_in_days(self):
        if self.date_consumed:
            return 0  # Or handle as appropriate if consumed
        delta = timezone.now().date() - self.date_added
        return delta.days

    @property
    def age(self):
        if self.date_consumed:
            return "Consumed"  # Or handle as appropriate

        today = timezone.now().date()
        delta = today - self.date_added

        if delta.days == 0:
            return "Today"

        years = delta.days // 365
        remaining_days_after_years = delta.days % 365
        months = remaining_days_after_years // 30
        days = remaining_days_after_years % 30

        age_parts = []
        if years > 0:
            age_parts.append(f"{years} year{'s' if years > 1 else ''}")
        if months > 0:
            age_parts.append(f"{months} month{'s' if months > 1 else ''}")
        if days > 0 or (years == 0 and months == 0):  # Show days if it's the only unit or if non-zero
            age_parts.append(f"{days} day{'s' if days > 1 else ''}")

        return ", ".join(age_parts) if age_parts else "Today"

    def __str__(self):
        return self.meal_name  # Updated to return the meal_name string directly
