# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-09 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_teacher_faculty'),
        ('school', '0004_auto_20181209_1720'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='teacher',
        ),
        migrations.AddField(
            model_name='course',
            name='teachers',
            field=models.ManyToManyField(related_name='courses', to='profiles.Teacher'),
        ),
    ]