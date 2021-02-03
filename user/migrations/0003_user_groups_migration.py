
from django.contrib.auth.models import ContentType, Group
from django.db import migrations


class Migration(migrations.Migration):
    def group_permissions(apps, schema_editor):
        custom_content_type = ContentType.objects.filter(app_label='custom')
        if not custom_content_type.exists():
            custom_content_type = ContentType.objects.create(
                model='custom', app_label='custom')
        else:
            custom_content_type = custom_content_type.first()
        groups = [
            {'name': "Admin"},
            {'name': "Management"},
            {'name': "Finance"}
        ]

        for group in groups:
            user_group = Group.objects.filter(name=group['name'])
            if user_group is not None:
                user_group = Group.objects.create(name=group['name'])
            else:
                user_group = user_group.first()

    dependencies = [
        ('user', '0002_auto_20201211_1227'),
    ]

    operations = [
        migrations.RunPython(group_permissions),
    ]
