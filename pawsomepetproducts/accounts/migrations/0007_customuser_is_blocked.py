# Generated by Django 4.2.14 on 2024-08-09 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]
