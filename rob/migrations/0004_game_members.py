# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-02 16:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rob', '0003_remove_player_games'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='members',
            field=models.ManyToManyField(through='rob.Selection', to='rob.Player'),
        ),
    ]
