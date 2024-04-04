# Generated by Django 4.2.11 on 2024-04-04 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('File_Ninja', '0005_alter_subscriptions_premium_pack_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptions',
            name='premium_pack',
        ),
        migrations.RemoveField(
            model_name='subscriptions',
            name='value_pack',
        ),
        migrations.AddField(
            model_name='subscriptions',
            name='cost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='subscriptions',
            name='description',
            field=models.TextField(default='No description available'),
        ),
        migrations.AddField(
            model_name='subscriptions',
            name='offer_name',
            field=models.CharField(default='No offer name available', max_length=100),
        ),
        migrations.AddField(
            model_name='subscriptions',
            name='validity',
            field=models.IntegerField(default=30),
        ),
    ]