# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 16:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20170620_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='productinorder',
            name='session_key',
            field=models.CharField(blank=True, default=None, max_length=128, null=True),
        ),
    ]
