from django.db import migrations


def populate_roles(apps, schema_editor):
    CustomUser = apps.get_model('users', 'CustomUser')
    for user in CustomUser.objects.all():
        if user.is_superuser:
            user.role = 'admin'
        else:
            user.role = 'customer'
        user.save()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0004_remove_customuser_is_customer_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_roles),
    ]
