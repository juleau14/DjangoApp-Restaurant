
from multiprocessing.sharedctypes import Value
from secrets import choice
from wsgiref.validate import validator
from xml.parsers.expat import model
from django.db import models
import django.utils.timezone
from django.core.validators import MaxLengthValidator, MinLengthValidator
import datetime


class Reservation(models.Model):
    NB_PEOPLE_CHOICES = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
    ]
    
    HOUR_CHOICES = [
        ('M1', '12:00'),
        ('M2', '12:15'),
        ('M3', '12:30'),
        ('M4', '12:45'),
        ('D1', '20:00'),
        ('D2', '20:15'),
        ('D3', '20:30'),
        ('D4', '20:45'),
    ]

    HOUR_TRAD = {
        'M1': '12:00',
        'M2': '12:15',
        'M3': '12:30',
        'M4': '12:45',
        'D1': '20:00',
        'D2': '20:15',
        'D3': '20:30',
        'D4': '20:45',
        }

    STATE_CHOICES = [
        ('0', 'En attente'),
        ('1', 'Accepté'),
        ('2', 'Refusé'),
    ]

    name = models.fields.CharField(max_length=20, validators=[MaxLengthValidator(20)])
    mail = models.fields.EmailField(max_length=100, validators=[MaxLengthValidator(100)])
    phone_number = models.fields.CharField(max_length=10, default="", validators=[MaxLengthValidator(10), MinLengthValidator(10)])
    
    nb_people = models.fields.CharField(max_length=2, default=1, choices=NB_PEOPLE_CHOICES)
    resa_date = models.fields.DateField(default=django.utils.timezone.now)
    hour = models.fields.CharField(max_length=2, choices=HOUR_CHOICES)

    accepted = models.fields.CharField(max_length=1, choices=STATE_CHOICES, default='0') # 0 en attente / 1 acceptée / 2 refusée

    def __str__(self):
        return f'{self.name}'


class Client(models.Model):
    name = models.fields.CharField(max_length=100, default='')
    phone_number = models.fields.CharField(max_length=10, default='')
    nb_reservations = models.fields.IntegerField(default=0)
    comment = models.fields.TextField(max_length=1000, default='')
    warning = models.fields.BooleanField(default=False)


class Holidays(models.Model):
    name = models.fields.CharField(max_length=100, default='')
    begin = models.fields.DateField(default=django.utils.timezone.now)
    end = models.fields.DateField(default=django.utils.timezone.now)


class FullService(models.Model):
    MEAL_CHOICES = [
        ('M', 'Midi'),
        ('D', 'Diner'),
    ]

    date = models.fields.DateField(default = django.utils.timezone.now)
    meal_type = models.fields.CharField(max_length=1, default="M", choices=MEAL_CHOICES)