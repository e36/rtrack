# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rtrack', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userreportlink',
            name='name',
            field=models.ForeignKey(to='rtrack.Username'),
            preserve_default=True,
        ),
    ]
