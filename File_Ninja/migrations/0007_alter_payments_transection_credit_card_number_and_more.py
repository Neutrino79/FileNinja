# Generated by Django 4.2.11 on 2024-04-09 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('File_Ninja', '0006_remove_active_subscription_list_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments_transection',
            name='Credit_Card_Number',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='payments_transection',
            name='name_on_card',
            field=models.CharField(max_length=100, null=True),
        ),
    ]