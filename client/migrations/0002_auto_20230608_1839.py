# Generated by Django 3.2.9 on 2023-06-08 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='clientuser',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
