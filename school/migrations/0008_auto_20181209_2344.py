# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-09 23:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0007_auto_20181209_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examresult',
            name='score',
            field=models.IntegerField(default=999),
        ),
    ]