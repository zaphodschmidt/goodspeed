# Generated by Django 5.1.5 on 2025-01-19 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_building_timezone_parkingspot_end_datetime_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parkingspot',
            name='monthly',
        ),
        migrations.AddField(
            model_name='parkingspot',
            name='occupied_by_lpn',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='parkingspot',
            name='reserved_by_lpn',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
