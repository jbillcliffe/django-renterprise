# Generated by Django 4.2.13 on 2024-05-23 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0009_alter_customer_address_line_three_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address_line_three',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='address_line_two',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]