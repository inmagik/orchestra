# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0009_auto_20140806_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='last_exception',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='operation',
            name='last_run',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='operation',
            name='last_run_ok',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
