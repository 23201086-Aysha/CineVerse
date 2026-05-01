from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_to_watchlist, name='add_to_watchlist'),
    path('', views.watchlist_view, name='watchlist_view'),
]
