# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-20 06:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0005_auto_20191019_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='order_key',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='порядок'),
        ),
        migrations.AlterField(
            model_name='taskitem',
            name='order_key',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='порядок'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='order_key',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='порядок'),
        ),
    ]
