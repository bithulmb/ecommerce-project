# Generated by Django 4.2.14 on 2024-08-29 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0002_rename_is_active_coupon_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='discount',
            new_name='discount_percent',
        ),
    ]
