# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-12 12:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0004_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='embargo',
            field=models.DateField(blank=True, null=True),
        ),
    ]