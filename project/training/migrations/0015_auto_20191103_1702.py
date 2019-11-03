# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-03 17:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0014_auto_20191103_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='ace_show_input',
            field=models.BooleanField(default=False, verbose_name='Отображать ввод'),
        ),
        migrations.AlterField(
            model_name='content',
            name='ace_content',
            field=models.TextField(blank=True, null=True, verbose_name='Редактор'),
        ),
        migrations.AlterField(
            model_name='content',
            name='ace_input',
            field=models.TextField(blank=True, null=True, verbose_name='Ввод'),
        ),
    ]