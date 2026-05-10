from django.urls import path
from . import views

app_name = 'watchlist'

urlpatterns = [
    path('add/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove/<int:item_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('', views.watchlist_view, name='watchlist_view'),
]
