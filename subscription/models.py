from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]

    DEFAULT_PLANS = [
        {
            'name': 'Free Plan',
            'plan_type': 'free',
            'price': 0.00,
            'duration_days': 99999,
            'features': {
                'unlimited_reviews': False,
                'priority_support': False,
                'exclusive_content': False,
            },
        },
        {
            'name': 'Basic Plan',
            'plan_type': 'basic',
            'price': 299.00,
            'duration_days': 30,
            'features': {
                'unlimited_reviews': True,
                'priority_support': False,
                'exclusive_content': False,
            },
        },
        {
            'name': 'Premium Plan',
            'plan_type': 'premium',
            'price': 599.00,
            'duration_days': 30,
            'features': {
                'unlimited_reviews': True,
                'priority_support': True,
                'exclusive_content': True,
            },
        },
    ]

    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration_days = models.IntegerField(default=30)  # For recurring subscriptions
    features = models.JSONField(default=dict)  # Store features as JSON, e.g., {'unlimited_reviews': True, 'priority_support': False}
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ৳{self.price}"

    @classmethod
    def sync_default_plans(cls):
        plans = []
        for plan_data in cls.DEFAULT_PLANS:
            plan, _ = cls.objects.update_or_create(
                plan_type=plan_data['plan_type'],
                defaults={
                    'name': plan_data['name'],
                    'price': plan_data['price'],
                    'duration_days': plan_data['duration_days'],
                    'features': plan_data['features'],
                    'is_active': True,
                }
            )
            plans.append(plan)
        return plans

    @classmethod
    def get_default_plan(cls, plan_type):
        return cls.objects.filter(plan_type=plan_type, is_active=True).first()
class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    auto_renew = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=100, blank=True)  # e.g., 'stripe', 'paypal'

    def __str__(self):
        return f"{self.user.username} - {self.plan.name if self.plan else 'No Plan'}"

    def is_expired(self):
        if self.end_date:
            return timezone.now() > self.end_date
        return False

    def has_feature(self, feature_key):
        if not self.plan:
            return False
        return self.plan.features.get(feature_key, False)
