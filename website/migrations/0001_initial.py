# Generated by Django 4.1.1 on 2022-09-29 08:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('phone_number', models.CharField(default='', max_length=10)),
                ('nb_reservations', models.IntegerField(default=0)),
                ('comment', models.TextField(default='', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('mail', models.EmailField(max_length=100)),
                ('phone_number', models.CharField(default='', max_length=10)),
                ('nb_people', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], default=1, max_length=2)),
                ('resa_date', models.DateField(default=django.utils.timezone.now)),
                ('hour', models.CharField(choices=[('M1', '12:00'), ('M2', '12:15'), ('M3', '12:30'), ('M4', '12:45'), ('D1', '20:00'), ('D2', '20:15'), ('D3', '20:30'), ('D4', '20:45')], max_length=2)),
                ('accepted', models.CharField(choices=[('0', 'En attente'), ('1', 'Accepté'), ('2', 'Refusé')], default='0', max_length=1)),
            ],
        ),
    ]
