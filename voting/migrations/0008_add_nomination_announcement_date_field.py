# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-18 13:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0007_nomination_gpa'),
    ]

    operations = [
        migrations.AddField(
            model_name='sacyear',
            name='election_nomination_announcement_datetime',
            field=models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0625\u0639\u0644\u0627\u0646 \u0627\u0644\u062a\u0631\u0634\u064a\u062d\u0627\u062a'),
        ),
    ]