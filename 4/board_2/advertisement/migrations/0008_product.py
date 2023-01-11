# Generated by Django 4.0.5 on 2023-01-10 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0007_advertisementtype_advertisement_adv_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
    ]
