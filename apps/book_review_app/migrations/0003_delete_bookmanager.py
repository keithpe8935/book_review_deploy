# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-23 09:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_review_app', '0002_bookmanager'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BookManager',
        ),
    ]
