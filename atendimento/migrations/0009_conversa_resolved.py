# Generated by Django 5.0.6 on 2024-05-21 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atendimento', '0008_remove_conversa_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversa',
            name='resolved',
            field=models.BooleanField(default=False),
        ),
    ]
