# Generated by Django 4.2.3 on 2023-08-09 19:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=models.UUIDField(default=models.Func('gen_random_uuid'), editable=False), editable=False, primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=200, null=True, verbose_name='Naran Propriu')),
                ('lastname', models.CharField(max_length=200, null=True, verbose_name='Apelidu')),
                ('pob', models.CharField(blank=True, max_length=100, null=True, verbose_name='Fatin Moris')),
                ('dob', models.DateTimeField(blank=True, null=True, verbose_name='Data Moris')),
                ('sex', models.CharField(choices=[('Mane', 'Mane'), ('Feto', 'Feto')], max_length=10, null=True, verbose_name='Sexu')),
                ('is_active', models.BooleanField(default=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='Profile')),
                ('datetime', models.DateTimeField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('user_created', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_created', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]