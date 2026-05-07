from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import SubscriptionPlan, UserSubscription

@login_required
def subscription_plans(request):
    plans = SubscriptionPlan.sync_default_plans()
    user_subscription = UserSubscription.objects.filter(user=request.user, is_active=True).first()

    # Format features for display so package benefits vary by tier
    for plan in plans:
        feature_list = []
        if plan.plan_type == 'free':
            feature_list.append(('Reviews per month', '10 reviews'))
        elif plan.plan_type == 'basic':
            feature_list.append(('Reviews per month', '50 reviews'))
        else:
            feature_list.append(('Reviews per month', 'Unlimited reviews'))

        feature_list.append(('Priority support', 'Yes' if plan.features.get('priority_support') else 'No'))
        feature_list.append(('Exclusive content', 'Yes' if plan.features.get('exclusive_content') else 'No'))
        feature_list.append(('Auto-renew', 'Optional'))

        plan.feature_list = feature_list

    return render(request, 'subscription_plans.html', {
        'plans': plans,
        'user_subscription': user_subscription
    })

@login_required
def subscribe(request, plan_id):
    SubscriptionPlan.sync_default_plans()
    plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)

    # Check if user already has an active subscription
    existing_subscription = UserSubscription.objects.filter(user=request.user, is_active=True).first()
    if existing_subscription:
        messages.error(request, "You already have an active subscription. Please manage it first.")
        return redirect('subscription:plans')

    # Check if user has an existing inactive subscription and update it, or create new one
    subscription, created = UserSubscription.objects.get_or_create(
        user=request.user,
        defaults={
            'plan': plan,
            'start_date': timezone.now(),
            'end_date': timezone.now() + timedelta(days=plan.duration_days),
            'is_active': True,
            'auto_renew': False
        }
    )

    if not created:
        # Update existing subscription
        subscription.plan = plan
        subscription.start_date = timezone.now()
        subscription.end_date = timezone.now() + timedelta(days=plan.duration_days)
        subscription.is_active = True
        subscription.save()

    messages.success(request, f"Successfully subscribed to {plan.name}!")
    return redirect('subscription:plans')

@login_required
def my_subscription(request):
    subscription = UserSubscription.objects.filter(user=request.user, is_active=True).first()

    # Format features for display if subscription exists
    if subscription and subscription.plan:
        feature_list = []
        if subscription.plan.plan_type == 'free':
            feature_list.append(('Reviews per month', '10 reviews'))
        elif subscription.plan.plan_type == 'basic':
            feature_list.append(('Reviews per month', '50 reviews'))
        else:
            feature_list.append(('Reviews per month', 'Unlimited reviews'))

        feature_list.append(('Priority support', 'Yes' if subscription.plan.features.get('priority_support') else 'No'))
        feature_list.append(('Exclusive content', 'Yes' if subscription.plan.features.get('exclusive_content') else 'No'))
        feature_list.append(('Auto-renew', 'Optional'))
        subscription.plan.feature_list = feature_list

    return render(request, 'my_subscription.html', {
        'subscription': subscription
    })

@login_required
def cancel_subscription(request):
    subscription = UserSubscription.objects.filter(user=request.user, is_active=True).first()
    if subscription:
        subscription.is_active = False
        subscription.save()
        messages.success(request, "Your subscription has been cancelled.")
    else:
        messages.error(request, "No active subscription found.")
    return redirect('subscription:my_subscription')

# Admin view to create plans (could be moved to admin)
@login_required
def create_plan(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('subscription:plans')

    if request.method == 'POST':
        name = request.POST.get('name')
        plan_type = request.POST.get('plan_type')
        price = request.POST.get('price')
        duration_days = request.POST.get('duration_days')

        SubscriptionPlan.objects.create(
            name=name,
            plan_type=plan_type,
            price=price,
            duration_days=duration_days,
            features={
                'unlimited_reviews': plan_type in ['basic', 'premium'],
                'priority_support': plan_type == 'premium',
                'exclusive_content': plan_type == 'premium'
            }
        )
        messages.success(request, "Plan created successfully!")
        return redirect('subscription:plans')

    return render(request, 'create_plan.html')