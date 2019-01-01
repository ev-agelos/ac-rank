# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-08 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laptimes', '0013_auto_20180407_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='setup',
            name='damp_bump_hf',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='setup',
            name='damp_bump_hr',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='setup',
            name='damp_fast_bump_hf',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='setup',
            name='damp_fast_bump_hr',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='setup',
            name='damp_fast_rebound_hf',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='setup',
            name='damp_fast_rebound_hr',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='setup',
            name='damp_rebound_hf',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='setup',
            name='damp_rebound_hr',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='setup',
            name='rod_length_hf',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='setup',
            name='rod_length_hr',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='setup',
            name='spring_rate_hf',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='setup',
            name='spring_rate_hr',
            field=models.SmallIntegerField(null=True),
        ),
    ]