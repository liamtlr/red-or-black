# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-05 18:27
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rob', '0016_auto_20170205_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='previous_colours',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default=[], max_length=100, null=True), blank=True, null=True, size=None),
        ),
    ]