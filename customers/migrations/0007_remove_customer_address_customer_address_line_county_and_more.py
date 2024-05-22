# Generated by Django 4.2.13 on 2024-05-22 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_alter_customer_options_customer_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='address',
        ),
        migrations.AddField(
            model_name='customer',
            name='address_line_county',
            field=models.CharField(default='X', max_length=200),
        ),
        migrations.AddField(
            model_name='customer',
            name='address_line_one',
            field=models.CharField(default='X', max_length=200),
        ),
        migrations.AddField(
            model_name='customer',
            name='address_line_three',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='address_line_town',
            field=models.CharField(default='X', max_length=200),
        ),
        migrations.AddField(
            model_name='customer',
            name='address_line_two',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(default='X', max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='postcode',
            field=models.CharField(default='XX20 2XX', max_length=8),
        ),
    ]