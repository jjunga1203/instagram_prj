# Generated by Django 4.2.11 on 2024-04-22 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_profile_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_url',
            field=models.TextField(default=''),
        ),
    ]
