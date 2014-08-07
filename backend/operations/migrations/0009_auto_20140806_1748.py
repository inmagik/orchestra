# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import orchestra_core.utils


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0008_operation_workflow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operation',
            old_name='assigned_id',
            new_name='oid',
        ),
        migrations.AddField(
            model_name='workflow',
            name='oid',
            field=models.CharField(default=orchestra_core.utils.generate_uuid, max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='workflow',
            name='assigned_id',
        ),
    ]
