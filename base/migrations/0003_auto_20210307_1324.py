# Generated by Django 3.1.5 on 2021-03-07 07:54

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20210307_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='public_id',
            field=models.CharField(default=base.models.public_id_fun, max_length=25, unique=True),
        ),
    ]
