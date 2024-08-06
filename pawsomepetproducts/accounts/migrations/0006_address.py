# Generated by Django 4.2.14 on 2024-08-05 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_customuser_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line1', models.CharField(max_length=50)),
                ('address_line2', models.CharField(blank=True, max_length=50)),
                ('town', models.CharField(max_length=40)),
                ('city', models.CharField(max_length=40)),
                ('state', models.CharField(max_length=40)),
                ('pincode', models.CharField(max_length=10)),
                ('contact_number', models.CharField(max_length=20)),
                ('is_default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
