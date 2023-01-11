# Generated by Django 4.0.5 on 2023-01-07 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0003_advertisement_created_at_advertisement_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='price',
            field=models.FloatField(default=0, verbose_name='цена'),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='views_count',
            field=models.IntegerField(default=0, verbose_name='количество просмотров'),
        ),
    ]