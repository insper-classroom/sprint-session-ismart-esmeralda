# Generated by Django 5.0.6 on 2024-05-21 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atendimento', '0007_conversa_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversa',
            name='uuid',
        ),
    ]
