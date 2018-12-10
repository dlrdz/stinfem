# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-09 17:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_auto_20181209_1711'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='weight',
            new_name='credit',
        ),
        migrations.AddField(
            model_name='course',
            name='code',
            field=models.CharField(default=4, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
