# Generated by Django 4.2.14 on 2024-08-19 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_orderproduct_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Approved', 'Approved'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned')], default='New', max_length=20),
        ),
    ]
