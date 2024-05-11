# Generated by Django 4.2.13 on 2024-05-11 14:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_customernote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='unique_id',
        ),
        migrations.AddField(
            model_name='customer',
            name='customer_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
