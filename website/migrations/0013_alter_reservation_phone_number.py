# Generated by Django 4.1.2 on 2022-11-01 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_client_first_name_alter_client_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='phone_number',
            field=models.CharField(default='', max_length=10),
        ),
    ]
