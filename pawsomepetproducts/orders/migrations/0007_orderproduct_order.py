# Generated by Django 4.2.14 on 2024-08-15 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_orderproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order'),
        ),
    ]
