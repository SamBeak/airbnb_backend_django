# Generated by Django 5.0.3 on 2024-03-22 10:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('experiences', '0001_initial'),
        ('medias', '0001_initial'),
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='rooms.room'),
        ),
        migrations.AddField(
            model_name='video',
            name='experience',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='experiences.experience'),
        ),
    ]
