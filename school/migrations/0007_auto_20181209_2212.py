# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-09 22:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_auto_20181209_2119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='subject',
            new_name='course',
        ),
    ]
