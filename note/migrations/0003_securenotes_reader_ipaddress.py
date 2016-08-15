# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0002_auto_20151006_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='securenotes',
            name='reader_ipaddress',
            field=models.TextField(null=True, verbose_name=b'Readers IP address', blank=True),
            preserve_default=True,
        ),
    ]
