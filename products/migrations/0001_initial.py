# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('index', models.PositiveIntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(default=b'', null=True, blank=True)),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('selling', models.BooleanField(default=True)),
                ('price', models.FloatField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='products.Category', null=True)),
                ('seller', models.ForeignKey(to='users.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='SavedSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('query', models.CharField(max_length=200)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='products.Category', null=True)),
                ('user', models.ForeignKey(to='users.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(related_name='buyer', to='users.Profile')),
                ('product', models.ForeignKey(to='products.Product')),
                ('seller', models.ForeignKey(related_name='seller', to='users.Profile')),
            ],
        ),
    ]
