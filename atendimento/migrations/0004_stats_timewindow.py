# Generated by Django 5.0.6 on 2024-06-01 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atendimento', '0003_conversa_is_avaliada'),
    ]

    operations = [
        migrations.AddField(
            model_name='stats',
            name='timewindow',
            field=models.DateField(auto_now=True),
        ),
    ]
