# Generated by Django 3.1.4 on 2021-01-26 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20210125_1514'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='order_by',
            new_name='customer',
        ),
    ]
