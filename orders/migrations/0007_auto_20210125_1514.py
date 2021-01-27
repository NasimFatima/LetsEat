# Generated by Django 3.1.4 on 2021-01-25 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20210125_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.IntegerField(choices=[(1, 'PENDING'), (2, 'COMPLETE')], default=1),
        ),
    ]