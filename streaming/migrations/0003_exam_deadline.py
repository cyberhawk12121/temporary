# Generated by Django 2.1.7 on 2020-05-17 05:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0002_auto_20200516_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='deadline',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
