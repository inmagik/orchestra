# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0003_auto_20140805_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='args',
            field=jsonfield.fields.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
