# Generated by Django 5.1.3 on 2024-11-06 20:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_remove_cartitem_customer_cartitem_cart_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='customer.customer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
