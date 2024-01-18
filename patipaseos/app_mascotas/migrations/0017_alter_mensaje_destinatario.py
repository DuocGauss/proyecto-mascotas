# Generated by Django 4.2.9 on 2024-01-17 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_mascotas', '0016_rename_message_mensaje'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensaje',
            name='destinatario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensaje_recibido', to='app_mascotas.cuidador'),
        ),
    ]