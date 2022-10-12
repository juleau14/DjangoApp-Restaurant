
from cProfile import label
from dataclasses import fields
import datetime
from email.policy import default
from pyexpat import model
from random import choices
from tkinter import Widget
from django import forms
from website.models import Reservation, Client, Holidays, FullService


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
        exclude = ('accepted', 'meal_type')

        labels = {
            "name": "Nom",
            "mail": "E-mail",
            "phone_number": "Tél.",
            "resa_date": "Date",
            "hour": "Heure",
            "nb_people": "Nombre de personnes",
            "comment": "Commentaires",
        }

        widgets = {
            'resa_date': forms.DateInput(attrs={'type': 'date'}),
        }


class LoginForm(forms.Form):
    username = forms.fields.CharField(max_length=100, label='Nom d utilisateur')
    password = forms.fields.CharField(max_length=100, widget=forms.PasswordInput(), label='Mot de passe')


class EditCommentForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('name', 'phone_number', 'nb_reservations',)
        
        labels = {
            "comment": "Commentaire client",
        }

    widgets = {
        'comment': forms.Textarea(attrs={'value': 'comment', 'style':'resize:none;'})
    }


class HolidaysForm(forms.ModelForm):
    class Meta:
        model = Holidays
        fields = '__all__'
        labels = {
            "name": "Nom",
            "begin": "Date de début",
            "end": "Date de fin",
        }

        widgets = {
            'begin': forms.DateInput(attrs={'type': 'date'}),
            'end': forms.DateInput(attrs={'type': 'date'}),
        }


class FullServiceForm(forms.ModelForm):
    class Meta:
        model = FullService
        fields = '__all__'
        labels = {
            "date": "Date",
            "meal_type": "Type de repas",
        }

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class FiltersForm(forms.Form):
    MEAL_CHOICES = [
        ("A", "Tous"),
        ("M", "Midi"),
        ("D", "Soir"),
    ]

    date = forms.fields.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))
    meal_type = forms.ChoiceField(label='Type repas' ,choices=MEAL_CHOICES)
