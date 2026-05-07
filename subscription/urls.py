from django.urls import path
from . import views

app_name = 'subscription'

urlpatterns = [
    path('', views.subscription_plans, name='subscription_home'),
    path('plans/', views.subscription_plans, name='plans'),
    path('subscribe/<int:plan_id>/', views.subscribe, name='subscribe'),
    path('my-subscription/', views.my_subscription, name='my_subscription'),
    path('cancel/', views.cancel_subscription, name='cancel_subscription'),
    path('create-plan/', views.create_plan, name='create_plan'),
]