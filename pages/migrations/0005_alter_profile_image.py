# Generated by Django 5.2.3 on 2025-06-19 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_book_status_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics/'),
        ),
    ]
