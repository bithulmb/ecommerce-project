# Generated by Django 4.2.14 on 2024-08-13 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_customuser_is_blocked"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="name",
            field=models.CharField(max_length=30, null=True),
        ),
    ]
