# Generated by Django 4.2.14 on 2024-08-23 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_reviewrating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewrating',
            old_name='ReviewRating',
            new_name='rating',
        ),
    ]
