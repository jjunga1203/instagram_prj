# Generated by Django 4.2.11 on 2024-04-24 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(max_length=1000, upload_to='images/'),
        ),
    ]