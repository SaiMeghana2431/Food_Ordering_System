# Generated by Django 5.1.3 on 2024-11-17 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_remove_cartitem_ordered_remove_cartitem_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
