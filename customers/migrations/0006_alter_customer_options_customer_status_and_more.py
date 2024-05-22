# Generated by Django 4.2.13 on 2024-05-21 12:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_rename_customer_id_customer_customer_token'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['last_name', 'first_name']},
        ),
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.IntegerField(choices=[(0, 'Current'), (1, 'Deceased'), (2, 'Archived')], default=0),
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]