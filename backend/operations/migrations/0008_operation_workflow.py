# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0007_workflow'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='workflow',
            field=models.ForeignKey(blank=True, to='operations.Workflow', null=True),
            preserve_default=True,
        ),
    ]
