# Generated by Django 4.0.5 on 2023-01-07 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
