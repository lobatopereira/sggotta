# Generated by Django 4.2.3 on 2023-08-31 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_alter_pediduprodutu_totalpresu'),
    ]

    operations = [
        migrations.AddField(
            model_name='pediduprodutu',
            name='is_checked',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
