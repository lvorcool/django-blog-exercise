# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-09-11 21:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('getExercise', '0012_remove_comment_createdon'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='avatar',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='createtime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]