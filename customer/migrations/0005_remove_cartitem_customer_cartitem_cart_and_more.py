# Generated by Django 5.1.3 on 2024-11-06 20:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='customer',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='customer.cart'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]