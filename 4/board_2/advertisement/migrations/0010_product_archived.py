# Generated by Django 4.0.5 on 2023-01-10 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0009_product_created_at_product_discount_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]