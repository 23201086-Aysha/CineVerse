"""
URL configuration for cineverses project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
app_name  = 'movie_app'

urlpatterns = [
    path('movie_list/', views.movie_list, name='movie_list'),
    path('', lambda request: redirect('movie_app:movie_list')),
    path('movie_detail/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('edit_movie/<int:pk>/', views.edit_movie, name='edit_movie'),
    path('delete_movie/<int:pk>/', views.delete_movie, name='delete_movie'),
]


