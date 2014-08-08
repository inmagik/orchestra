# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0010_auto_20140807_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='last_end',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
