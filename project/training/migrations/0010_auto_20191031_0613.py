# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-31 06:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0009_auto_20191031_0606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskitem',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, verbose_name='слаг'),
        ),
    ]