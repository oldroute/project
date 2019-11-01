# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-31 19:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0012_auto_20191031_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='training.Topic'),
        ),
        migrations.AlterField(
            model_name='content',
            name='type',
            field=models.CharField(choices=[('ace', 'код'), ('text', 'текст')], default='text', max_length=255),
        ),
    ]
