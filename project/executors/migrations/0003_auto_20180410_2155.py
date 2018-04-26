# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-10 16:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('executors', '0002_auto_20180410_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='executor',
            field=models.ForeignKey(blank=True, help_text='если не выбран то наследуется от родителя', null=True, on_delete=django.db.models.deletion.CASCADE, to='executors.Executor', verbose_name='Исполнитель'),
        ),
        migrations.AlterField(
            model_name='code',
            name='type',
            field=models.IntegerField(choices=[(1, 'Статичный'), (2, 'Исполняемый(компактный)'), (3, 'Исполняемый')], default=1, verbose_name='тип'),
        ),
        migrations.AlterField(
            model_name='executor',
            name='name',
            field=models.IntegerField(choices=[(0, 'Наследуется'), (1, 'Python 3.6')], unique=True, verbose_name='название'),
        ),
    ]