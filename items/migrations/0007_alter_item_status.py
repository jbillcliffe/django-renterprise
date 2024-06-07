# Generated by Django 4.2.13 on 2024-06-07 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_alter_item_item_serial_alter_item_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.IntegerField(choices=[(0, 'Available'), (1, 'Scrapped'), (2, 'Lost/Stolen'), (3, 'Sold'), (4, 'Needs Repairs')], default=0),
        ),
    ]