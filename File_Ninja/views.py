from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from File_Ninja.models import UserProfile
import logging
logger = logging.getLogger(__name__)
from File_Ninja.models import Subscriptions


def home(request):
    value_pack = Subscriptions.objects.filter(offer_name='Value_pack').first()
    premium_pack = Subscriptions.objects.filter(offer_name='Premium_pack').first()
    if value_pack:
        value_pack_cost = value_pack.cost
    else:
        value_pack_cost = None

    if premium_pack:
        premium_pack_cost = premium_pack.cost
    else:
        premium_pack_cost = None

    return render(request, 'index.html', {'value_pack_cost': value_pack_cost, 'premium_pack_cost': premium_pack_cost})


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


