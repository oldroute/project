# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-20 13:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0008_auto_20191120_0821'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0003_auto_20191117_2001'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupmember',
            options={'ordering': ['user__last_name'], 'verbose_name': 'участник', 'verbose_name_plural': 'участники'},
        ),
        migrations.RenameField(
            model_name='group',
            old_name='members',
            new_name='_members',
        ),
        migrations.AlterField(
            model_name='group',
            name='status',
            field=models.CharField(choices=[('0', 'открыто'), ('1', 'закрыто'), ('2', 'по кодовому слову')], default='1', max_length=255, verbose_name='вступление в группу'),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member', to='groups.Group'),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member', to=settings.AUTH_USER_MODEL, verbose_name='участник'),
        ),
        migrations.AlterUniqueTogether(
            name='groupcourse',
            unique_together=set([('group', 'course')]),
        ),
        migrations.AlterUniqueTogether(
            name='groupmember',
            unique_together=set([('group', 'user')]),
        ),
    ]
