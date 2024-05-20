# Generated by Django 4.2.13 on 2024-05-20 01:04

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_alter_item_item_serial_alter_itemtype_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemtype',
            name='image',
            field=cloudinary.models.CloudinaryField(default='placeholder', max_length=255, verbose_name='image'),
        ),
    ]