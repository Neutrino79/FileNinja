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
from File_Ninja.models import UserProfile
import logging
import json
logger = logging.getLogger(__name__)
from File_Ninja.models import Subscriptions


def home(request):
    subscription1 = Subscriptions.objects.get(pk=1)
    subscription2 = Subscriptions.objects.get(pk=2)
    sub_id=UserProfile.objects.get(user=request.user).subscription_id
    user_sub_cost=Subscriptions.objects.get(pk=sub_id).cost
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
        UserProfile.objects.create(user=user, email=email, password=password, full_name=full_name, dob=dob, number=number)

        return JsonResponse({'message': 'Registered successfully'}, status=200)


def payment(request):

    return render(request, 'payment.html')


@csrf_exempt
@require_POST
def checkout(request):
    print("In the checkpuut")
    data = json.loads(request.body)
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    payment_mode = data.get('payment_mode')
    credit_card_number = data.get('credit_card_number')
    name_on_card = data.get('name_on_card')
    country = data.get('country')
    state = data.get('state')
    zip = data.get('zip')
    email = data.get('email')
    print(first_name, last_name, payment_mode, credit_card_number, name_on_card, country, state, zip , email)

    return JsonResponse({'message': 'Checkout successful'})