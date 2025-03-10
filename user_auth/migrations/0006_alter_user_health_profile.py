# Generated by Django 5.1.4 on 2025-01-10 13:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0005_alter_user_full_name_alter_user_health_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='health_profile',
            field=models.JSONField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(500), django.core.validators.MinLengthValidator(8)]),
        ),
    ]
