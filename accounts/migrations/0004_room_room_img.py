# Generated by Django 4.0.1 on 2023-11-25 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_room_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_img',
            field=models.ImageField(blank=True, upload_to='room_img/'),
        ),
    ]
