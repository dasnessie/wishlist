# Generated by Django 3.0.9 on 2020-08-17 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0002_wish_unbuy_string'),
    ]

    operations = [
        migrations.AddField(
            model_name='wish',
            name='santa_nick',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
