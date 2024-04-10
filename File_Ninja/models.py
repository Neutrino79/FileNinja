from django.db import models
from django.contrib.auth.models import User


class Subscriptions(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    offer_name = models.CharField(max_length=100,default='No offer name available')
    cost = models.FloatField(default=0)
    validity = models.IntegerField(default=30)
    description = models.TextField(default='No description available')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, unique=True, null=True)
    password = models.CharField(max_length=100, null=True)
    full_name = models.CharField(max_length=200, null=True)
    profile_picture = models.URLField(null=True)
    locale = models.CharField(max_length=10, null=True)
    dob = models.DateField(null=True)  # Date of Birth field
    number = models.CharField(max_length=10, null=True)
    is_premium = models.CharField(max_length=3, default='NO')
    subscription = models.ForeignKey(Subscriptions, on_delete=models.SET_NULL, null=True )


class payments_transection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    payment_id = models.AutoField(primary_key=True)
    subscription = models.ForeignKey(Subscriptions, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    payment_mode = models.CharField(max_length=100)
    payment_date = models.DateField()
    Credit_Card_Number = models.CharField(max_length=16, null=True)
    name_on_card = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)



class active_subscription_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    subscription = models.ForeignKey(Subscriptions, on_delete=models.SET_NULL, null=True)
    payment_id=models.ForeignKey(payments_transection,on_delete=models.SET_NULL,null=True)


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()