# Generated by Django 4.2.14 on 2024-08-11 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_remove_cart_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='quanity',
            new_name='quantity',
        ),
    ]
