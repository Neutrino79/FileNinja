from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from File_Ninja.models import UserProfile


def home(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


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
            return JsonResponse({'message': 'Email already exists'}, status=400)

        user = User.objects.create_user(username=email, email=email, password=password)
        UserProfile.objects.create(user=user, email=email, password=password, full_name=full_name, dob=dob, number=number)

        return JsonResponse({'message': 'Registered successfully'}, status=200)


