# Generated by Django 4.0.5 on 2023-01-11 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0012_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', to='advertisement.product'),
        ),
    ]