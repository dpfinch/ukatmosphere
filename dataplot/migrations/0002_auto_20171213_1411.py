# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-13 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataplot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selected_site',
            name='sitechoice',
            field=models.CharField(max_length=200),
        ),
    ]