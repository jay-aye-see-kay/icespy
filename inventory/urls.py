from django.urls import path
from . import views

app_name = 'inventory'  # Added app_name

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('consume/<int:item_id>/', views.consume_meal_view, name='consume_meal'),
    path('edit/<int:item_id>/', views.edit_meal_view, name='edit_meal'),
    path('history/', views.consumed_history_view, name='consumed_history'),
]
