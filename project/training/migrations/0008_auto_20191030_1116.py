# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-30 11:16
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0007_auto_20191020_0647'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solution',
            old_name='best',
            new_name='version_best',
        ),
        migrations.RenameField(
            model_name='solution',
            old_name='versions',
            new_name='version_list',
        ),
        migrations.AddField(
            model_name='solution',
            name='progress',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Прогресс решения'),
        ),
        migrations.AddField(
            model_name='solution',
            name='status',
            field=models.CharField(choices=[('0', 'нет попыток'), ('1', 'тесты не пройдены'), ('2', 'часть тестов пройдены'), ('3', 'все тесты пройдены')], default='0', max_length=255, verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='solution',
            name='last_changes',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='последние изменения'),
        ),
        migrations.AlterField(
            model_name='solution',
            name='url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
