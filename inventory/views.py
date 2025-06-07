from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import MealItem, MealNameSuggestion
from .forms import AddMealForm

# Create your views here.

@login_required
def dashboard_view(request):
    if request.method == 'POST':
        form = AddMealForm(request.POST)
        if form.is_valid():
            meal_name_str = form.cleaned_data['meal_name']
            date_added = form.cleaned_data['date_added']
            number_of_containers = form.cleaned_data['number_of_containers']
            portions_per_container = form.cleaned_data['portions_per_container']
            note = form.cleaned_data['note']

            meal_name_suggestion, _ = MealNameSuggestion.objects.get_or_create(
                name=meal_name_str,
                defaults={'user': request.user} # Optional: associate suggestion with user
            )
            # If the meal_name_suggestion was created and associated with a user,
            # or if it existed and you want to ensure it's associated with the current user
            # (and it's not already associated with another user, which get_or_create handles by not updating if found)
            if not meal_name_suggestion.user:
                meal_name_suggestion.user = request.user
                meal_name_suggestion.save()


            for _ in range(number_of_containers):
                MealItem.objects.create(
                    user=request.user,
                    meal_name=meal_name_suggestion,
                    date_added=date_added,
                    portions_per_container=portions_per_container,
                    note=note
                )
            return redirect('dashboard')
    else:
        form = AddMealForm()
    
    meal_items = MealItem.objects.filter(user=request.user).order_by('-date_added', 'meal_name__name')
    context = {
        'meal_items': meal_items,
        'form': form
    }
    return render(request, 'dashboard.html', context)
