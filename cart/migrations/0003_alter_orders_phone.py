# Generated by Django 5.0 on 2024-01-17 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_alter_customeraddress_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='phone',
            field=models.BigIntegerField(),
        ),
    ]