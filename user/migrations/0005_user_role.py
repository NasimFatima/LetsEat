# Generated by Django 3.1.4 on 2020-12-17 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20201217_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]