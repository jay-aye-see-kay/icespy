from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import MealItem
from .forms import AddMealForm, EditMealForm

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

            for _ in range(number_of_containers):
                MealItem.objects.create(
                    user=request.user,
                    meal_name=meal_name_str, # Use the string directly
                    date_added=date_added,
                    portions_per_container=portions_per_container,
                    note=note
                )
            return redirect('inventory:dashboard')
    else:
        form = AddMealForm(initial={
            'date_added': timezone.now().date(),
            'number_of_containers': 1,
            'portions_per_container': 2
        })
    
    meals = MealItem.objects.filter(user=request.user, date_consumed__isnull=True).order_by('date_added')
    # Get distinct meal names from MealItem for the current user
    meal_name_suggestions = MealItem.objects.filter(user=request.user).values_list('meal_name', flat=True).distinct()
    
    context = {
        'meals': meals,
        'form': form,
        'meal_name_suggestions': meal_name_suggestions
    }
    return render(request, 'inventory/dashboard.html', context)

@login_required
@require_POST
def consume_meal_view(request, item_id):
    meal = get_object_or_404(MealItem, id=item_id, user=request.user) # Ensure user owns the meal
    meal.date_consumed = timezone.now().date()
    meal.consumed_by_user = request.user
    meal.save()
    return redirect('inventory:dashboard') # Changed to inventory:dashboard

@login_required
def edit_meal_view(request, item_id):
    meal = get_object_or_404(MealItem, id=item_id, user=request.user) # Ensure user owns the meal
    if request.method == 'POST':
        form = EditMealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            return redirect('inventory:dashboard') # Changed to inventory:dashboard
    else:
        form = EditMealForm(instance=meal)
    
    context = {
        'form': form,
        'meal': meal # Pass meal to template for context if needed (e.g., in heading)
    }
    return render(request, 'inventory/edit_meal.html', context)

@login_required
def consumed_history_view(request):
    consumed_meals = MealItem.objects.filter(
        user=request.user, 
        date_consumed__isnull=False
    ).order_by('-date_consumed')
    
    context = {
        'consumed_meals': consumed_meals
    }
    return render(request, 'inventory/consumed_history.html', context)
