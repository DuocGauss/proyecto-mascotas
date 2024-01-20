# Generated by Django 4.2.9 on 2024-01-19 22:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_mascotas', '0020_resena'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resena',
            name='calificacion',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
