# Generated by Django 4.0.5 on 2023-01-08 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0005_advertisementstatus_advertisement_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='status',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='advertisement', to='advertisement.advertisementstatus'),
        ),
    ]
