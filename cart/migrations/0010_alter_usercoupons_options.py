# Generated by Django 5.0 on 2024-01-25 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_usercoupons_is_active_usercoupons_is_used'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usercoupons',
            options={'ordering': ('-id',)},
        ),
    ]
