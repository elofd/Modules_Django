# Generated by Django 4.0.5 on 2023-01-08 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0006_alter_advertisement_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvertisementType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='advertisement',
            name='adv_type',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='advertisement', to='advertisement.advertisementtype'),
        ),
    ]
