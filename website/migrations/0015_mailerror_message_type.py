# Generated by Django 4.1 on 2022-11-21 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_mailerror'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailerror',
            name='message_type',
            field=models.CharField(default='', max_length=30),
        ),
    ]