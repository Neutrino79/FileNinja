from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, unique=True, null=True)
    password = models.CharField(max_length=100, null=True)
    full_name = models.CharField(max_length=200, null=True)
    profile_picture = models.URLField(null=True)
    locale = models.CharField(max_length=10, null=True)
    dob = models.DateField(null=True)  # Date of Birth field
    number = models.CharField(max_length=10, null=True)


