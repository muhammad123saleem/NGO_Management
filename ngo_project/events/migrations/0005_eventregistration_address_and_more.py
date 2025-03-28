# Generated by Django 5.2b1 on 2025-03-13 17:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_remove_eventregistration_member_count'),
        ('volunteer', '0002_volunteerassignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventregistration',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='eventregistration',
            name='member_count',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='eventregistration',
            name='participant_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='eventregistration',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='volunteer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='volunteer.volunteer'),
        ),
    ]
