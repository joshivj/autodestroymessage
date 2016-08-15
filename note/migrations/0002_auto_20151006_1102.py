# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='securenotes',
            name='read_date',
            field=models.DateTimeField(auto_now=True, null=True),
            preserve_default=True,
        ),
    ]
