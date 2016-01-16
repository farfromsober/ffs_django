# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20151127_0827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='seller',
        ),
    ]
