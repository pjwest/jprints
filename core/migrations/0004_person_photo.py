# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-19 10:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20160812_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='photo',
            field=models.ImageField(blank=True, upload_to='profile_images'),
        ),
    ]
