# Generated by Django 4.2.3 on 2023-08-28 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_pedidu_pediduprodutu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedidu',
            name='numerupakote',
        ),
        migrations.AddField(
            model_name='pedidu',
            name='kodigupedidu',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Kodigu Pedidu'),
        ),
    ]
