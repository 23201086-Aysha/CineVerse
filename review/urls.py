from django.urls import path
from . import views

urlpatterns = [
    path('movie/<int:movie_id>/', views.movie_reviews, name='movie_reviews'),
    path('add/<int:movie_id>/', views.add_review, name='add_review'),
    path('reply/<int:review_id>/', views.add_reply, name='add_reply'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
]