# Generated by Django 4.1.1 on 2022-09-29 10:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_hollydays'),
    ]

    operations = [
        migrations.CreateModel(
            name='Holidays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin', models.DateField(default=datetime.date(2100, 1, 1))),
                ('end', models.DateField(default=datetime.date(2100, 1, 1))),
            ],
        ),
    ]
