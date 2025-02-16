# Generated by Django 5.1.6 on 2025-02-16 01:57

import storages.backends.s3
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(storage=storages.backends.s3.S3Storage, upload_to='images/'),
        ),
    ]
