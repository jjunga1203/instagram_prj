# Generated by Django 4.2.11 on 2024-04-24 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='msg_user_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='msg_user_real_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]