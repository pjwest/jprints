# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-31 14:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20161212_1146'),
        ('publications', '0007_auto_20170125_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributor',
            name='number',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='contributor',
            name='publication',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='publications.Publication'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='book_series',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='publication',
            name='book_title',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='publication',
            name='contributors',
            field=models.ManyToManyField(related_name='contributes_to', through='publications.Contributor', to='core.Person'),
        ),
        migrations.AddField(
            model_name='publication',
            name='doi',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='publication',
            name='isbn',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='publication',
            name='issn_e',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='publication',
            name='issn_l',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='publication',
            name='issn_p',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='publication',
            name='issue',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='publication',
            name='journal',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='publication',
            name='keywords',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='pagerange',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='publication',
            name='pages',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='publication',
            name='place_of_pub',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='publication',
            name='publisher',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='publication',
            name='pubmedid',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='publication',
            name='suggestions',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='volume',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='publication',
            name='wosid',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='publication',
            name='publication_date',
            field=models.DateField(blank=True),
        ),
    ]
