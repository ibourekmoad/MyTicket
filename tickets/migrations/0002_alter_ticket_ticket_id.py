# Generated by Django 5.0.6 on 2024-05-24 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_id',
            field=models.CharField(max_length=7, null=True, unique=True),
        ),
    ]
