# Generated by Django 4.2.3 on 2023-09-08 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0010_pediduprodutu_is_checked'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidu',
            name='is_delivered',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='pediduprodutu',
            name='is_delivered',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
