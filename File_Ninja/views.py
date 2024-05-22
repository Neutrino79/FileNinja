from datetime import datetime, timedelta

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from File_Ninja.models import *
import logging
import json
logger = logging.getLogger(__name__)
from File_Ninja.models import Subscriptions
from django.utils import timezone
from django.db.models import ObjectDoesNotExist

def home(request):
    subscription1 = Subscriptions.objects.get(pk=2)
    subscription2 = Subscriptions.objects.get(pk=3)
    if request.user.is_authenticated:
        sub_id=UserProfile.objects.get(user=request.user).subscription_id
        user_sub_cost=Subscriptions.objects.get(pk=sub_id).cost
    else:
        sub_id = None
        user_sub_cost = None
    return render(request, 'index.html', {'user_sub_cost':user_sub_cost,'subscription1':subscription1,'subscription2':subscription2})


def login_view(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print("email=", email)
        print("password=", password)
        user = authenticate(request, username=email, password=password)
        print("user after authenticate=", user)

        if user is not None:
            print("user=", user)
            login(request, user)
            messages.success(request, f'Successfully logged in as {request.user.username}')
            return redirect('home')

        else:
            context['invalid_credentials'] = True
    return render(request, 'index.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def google_login_redirect(request):
    print("request = ",request)
    user = request.user
    print("user = ",user)
    social = user.social_auth.get(provider='google-oauth2')
    google_data = {
        'email': social.uid,
        'full_name': social.extra_data.get('name'),
        'profile_picture': social.extra_data.get('picture'),
        'locale': social.extra_data.get('locale'),
    }
    UserProfile.objects.update_or_create(user=user, defaults=google_data)
    messages.success(request, f'Successfully logged in as {request.user.username}')
    return redirect('home')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        full_name = request.POST.get('name')
        dob = request.POST.get('DOB')
        number = request.POST.get('number')

        if User.objects.filter(email=email).exists():
            print("email already exists")
            return JsonResponse({'message': 'Email already exists'}, status=400)

        user = User.objects.create_user(username=email, email=email, password=password)
        UserProfile.objects.create(user=user, email=email, password=password, full_name=full_name, dob=dob, number=number,subscription_id=1)

        return JsonResponse({'message': 'Registered successfully'}, status=200)


def payment(request):

    return render(request, 'payment.html')

def handle_feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        feedback = Feedback(name=name, email=email, subject=subject, message=message)
        feedback.save()
        print(JsonResponse({'success': True,'message': 'Feedback sent successfully'}))
        return JsonResponse({'success': True,'message': 'Feedback sent successfully'})


@csrf_exempt
@require_POST
def checkout(request):
    print("In the checkout")
    data = json.loads(request.body)
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    payment_mode = data.get('payment_mode')
    credit_card_number = data.get('credit_card_number')
    name_on_card = data.get('name_on_card')
    country = data.get('country')
    state = data.get('state')
    zip_code = data.get('zip')
    email = data.get('email')
    sub_id = data.get('sub_id')
    print(first_name, last_name, payment_mode, credit_card_number, name_on_card, country, state, zip_code , email , sub_id)

    # Create a new transaction in the payments_transection table
    payment = payments_transection.objects.create(
        user=request.user,
        first_name=first_name,
        last_name=last_name,
        payment_mode=payment_mode,
        payment_date=timezone.now(),
        Credit_Card_Number=credit_card_number,
        name_on_card=name_on_card,
        country=country,
        state=state,
        zip=zip_code,
        email=email,
        subscription_id=sub_id
    )
    payment.save()

    # Create a new active subscription in the active_subscription_list table
    start_date = datetime.now()
    end_date = start_date + timedelta(days=30)  # Assuming a subscription lasts for 30 days
    ''' active_subscription_list.objects.create(
        user=request.user,
        subscription_id=sub_id,
        start_date=start_date,
        end_date=end_date,
        payment_id = payment,
        email=email
    )'''
    try:
        # Try to get the existing record
        active_subscription = active_subscription_list.objects.get(email=email)
        # If it exists, update the fields
        active_subscription.start_date = start_date
        active_subscription.end_date = end_date
        active_subscription.subscription_id = sub_id
        active_subscription.payment_id = payment
        active_subscription.save()
    except ObjectDoesNotExist:
        # If it does not exist, create a new record
        active_subscription_list.objects.create(
            user=request.user,
            email=email,
            start_date=start_date,
            end_date=end_date,
            subscription_id=sub_id,
            payment_id=payment
        )


    # Update the user's profile with the new subscription ID and set the p/remium status
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.subscription_id = sub_id
    user_profile.is_premium = "YES"  # Assuming a successful checkout makes the user premium
    user_profile.save()

    return JsonResponse({'success': True, 'message': 'Checkout successful'})