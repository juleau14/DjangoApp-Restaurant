# Generated by Django 4.1.1 on 2022-09-30 06:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_alter_holidays_begin_alter_holidays_end'),
    ]

    operations = [
        migrations.CreateModel(
            name='FullService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('lunch_type', models.CharField(choices=[('M', 'Midi'), ('D', 'Diner')], default='M', max_length=1)),
            ],
        ),
    ]
