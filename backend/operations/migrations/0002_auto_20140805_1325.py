# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operation',
            old_name='operation',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='operation',
            name='task',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
