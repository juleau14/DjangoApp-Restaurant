from calendar import weekday
from http.client import ACCEPTED, HTTPResponse
from logging import NullHandler
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from website.forms import LoginForm, ReservationForm, EditClientForm, HolidaysForm, FullServiceForm, FiltersForm
from website.models import Reservation, Client, Holidays, FullService
from django.core.mail import send_mail
from django.conf import settings

from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import datetime


def redirect_home(request):
    return redirect('home')


def home(request):
    return render(request,
    'website/home.html',
    )


# fonctions de vérification de réservation
def date_is_past(date_form):    # vérifie si un date est passée
    if datetime.date.today() > date_form:
        return True
    else:
        return False

def day_is_monday_or_sunday(week_day):  # vérifie si la date tombe un lundi ou un dimanche
    if week_day == 0 or week_day == 6:
        return True
    else:
        return False

def reservation_on_unexisting_evening(meal_type, week_day, diner_closed_days):  # vérifie si la l'heure est un mardi ou mercredi soir
    if meal_type == "D" and week_day in diner_closed_days:
        return True
    else:
        return False

def reservation_is_too_late(meal_type, date_form): # vérifie si l'heure de reservation est moins d'une heure avant le début du service
    now = datetime.datetime.now()
    today = datetime.date.today()
    if today == date_form:
        if meal_type == "M":
            if now.hour + 1 >= 11:
                return True

        elif meal_type == "D":
            if now.hour + 1 >= 19:
                return True

    return False

def reservation_is_during_holidays(date_form):  # vérifie si la réservation tombe pendant une date de vacances
    all_holidays = Holidays.objects.all()
    for holidays in all_holidays:
        if holidays.begin < date_form < holidays.end:
            return True
    
    return False

def reservation_is_on_full_service(date_form, meal_type):           # vérifie si le service est complet
    full_services = FullService.objects.all()

    for service in full_services:
        if date_form == service.date and meal_type == service.meal_type:
            return True
        
    return False

def reservation_is_valid(meal_type, diner_closed_days, date_form):      # vérifie si la réservation est valide pour le restaurant, si non, retourne le message d'erreur correspondant au problème
    wrong_schedule_msg = "Désolé, votre demande de réservation ne correspond pas à nos horaires et/ou jours d ouverture."
    unexisting_date_msg = "Désolé, la date entrée n est pas valide."
    too_late_msg = "Désolé, il est trop tard pour réserver sur ce créneau horaire."
    holidays_msg = "Désolé, le restaurant sera en congées pendant cette période."
    full_service_msg = "Désolé, ce service est complet."
    
    try:               # on en tire le jour de la semaine correspondant                                 
        week_day = date_form.weekday()    
    except ValueError:                                          # si il y a une erreur alors date invalide, message d'erreur
        return unexisting_date_msg

    if date_is_past(date_form):                 # la date est passée
        return unexisting_date_msg
    
    elif day_is_monday_or_sunday(week_day):             # le jour tombe lundi ou dimanche
        return wrong_schedule_msg
    
    elif reservation_on_unexisting_evening(meal_type, week_day, diner_closed_days):         # la reservation est mardi ou mercredi soir
        return wrong_schedule_msg
    
    elif reservation_is_too_late(meal_type, date_form):                    # la reservation est une moins d'une heure avant le service
        return too_late_msg

    elif reservation_is_during_holidays(date_form):                 # la réservation tombe pendant une période de vacance
        return holidays_msg

    elif reservation_is_on_full_service(date_form, meal_type):      # la réservation tombe pendant un service complet 
        return full_service_msg

    else:                                                           # la réservation ne rencontre aucun problème, elle est valide
        return True

def translate_date(date_form):
    translated_date = ""

    weekday_dict = {
        0: "Lundi ",
        1: "Mardi ",
        2: "Mercredi ",
        3: "Jeudi ",
        4: "Vendredi ",
        5: "Samedi ",
        6: "Dimanche ",
    }

    month_dict = {
        1: " Janvier",
        2: " Février",
        3:  " Mars",
        4: " Avril",
        5: " Mai",
        6: " Juin",
        7: " Juillet",
        8: " Août",
        9: " Septembre",
        10: " Octobre",
        11: " Novembre",
        12: " Décembre",
    }

    weekday = weekday_dict[date_form.weekday()]
    day = date_form.day
    month = month_dict[date_form.month]

    translated_date = weekday + str(day) + month

    return translated_date


def maintenance(request):
    return render(request,
        'website/maintenance.html')


def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            meal_type = form.cleaned_data['hour'][0]        # repas du soir ou du midi (midi = 'M', soir = 'D')
            diner_closed_days = [1, 2]                      # jours ou le restaurant ferme le soir (mardi et mercredi)
            date_form = form.cleaned_data['resa_date']      # date de reservation (date_form et pas date pour ne pas entrer en conflit avec datetime)

            valid_return = reservation_is_valid(meal_type, diner_closed_days, date_form)    # valid return =True si valide ou le message d'erreur correspondant au problème
            
            if valid_return == True:                                # on test si la réservation est valide
                form.save()                                         # si oui on la sauvegarde dans la base de données
                name = form.cleaned_data['name']                    # on récupère le nom 
                hour = Reservation.HOUR_TRAD[form.cleaned_data['hour']]                  # on récupère l'heure de la resa
                nb_people = form.cleaned_data['nb_people']          # on récupère le nb de personnes
                mail = form.cleaned_data['mail']                    # on récupère le mail du client
                phone_num = form.cleaned_data['phone_number']       # on récupère le numéro du client
                
                html_content = render_to_string("website/mails/confirm_reservation_mail.html",
                {'nb_people': nb_people,
                'name': name,
                'date_form': translate_date(date_form),
                'hour': hour,
                'phone_number': phone_num,
                },
                )

                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                    subject='[Restaurant L\'Air de  Famille - Toulouse] Accusé de réception',
                    body=text_content,
                    from_email= settings.EMAIL_HOST_USER,
                    to=[mail],
                )

                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=False)
                
                try:                                                                # si le client est déjà venu on ajoute une reservation
                    client = Client.objects.get(phone_number=phone_num)
                    client.nb_reservations += 1
                    
                    if client.first_name == '':                                      # si le client n'avais pas de prénom on lui en ajoute un sur cette réservation
                        client.first_name = form.cleaned_data['first_name']
                    
                    client.save()
                except:                                                  # si le numéro est inconnu on génère une nouvelle fiche client
                    new_client = Client()
                    new_client.name = form.cleaned_data['name']
                    new_client.phone_number = phone_num
                    new_client.nb_reservations += 1
                    new_client.save()

                return redirect('confirmation-page',
                mail,
                )
            
            else:                                       # si la resa n'est pas correcte, on raffiche le formulaire avec le message d'erreur renvoyé par la fonction de validation
                return render(request,
                'website/reservation.html',
                {'form': form, 'message': valid_return},
                )

        else:
            return render(request,
            'website/reservation.html',
            {'form': form, 'message': ''},
            ) 

    else:
        form = ReservationForm()

        return render(request,
        'website/reservation.html',
        {'form': form}
        )

        # return redirect('maintenance')


def reservation_confirmated(request, mail):
    return render(request,
    'website/confirmation.html',
    {'mail': mail},
    )


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                return redirect('display-reservations-list')
            else:
                message = 'Identifiants invalides.'
                
                return render(request,
                'website/login_page.html',
                {'form': form, 'message': message},
                )
        
        else:
            message = 'Identifiants invalides.'

            form = LoginForm()

            return render(request,
            'website/login_page.html',
            {'form': form, 'message': message},
            )
    
    else:
        
        form = LoginForm()

        message = ''

        return render(request,
        'website/login_page.html',
        {'form': form, 'message': message},
        )


def logout_page(request):
    logout(request)

    return redirect('home')


@login_required()
def display_reservations_list(request):
    Clients = Client.objects.all()
    if request.method == 'POST':
        form = FiltersForm(request.POST)
        
        if form.is_valid():
            date = form.cleaned_data['date']
            meal_type = form.cleaned_data['meal_type']
            all_reservations = Reservation.objects.all()
            filtered_reservations = []
            
            for reservation in all_reservations:
                if meal_type == "A":
                    if reservation.resa_date == date and reservation.accepted == '0':
                        filtered_reservations.append(reservation)
                else:
                    if reservation.resa_date == date and reservation.hour[0] == meal_type and reservation.accepted == '0':
                        filtered_reservations.append(reservation)

            print(filtered_reservations)

            if len(filtered_reservations) == 0:
                message = "Aucune réservation à afficher."
            else:
                message = ""

            return render(request,
            'website/waiting_reservations_list.html',
            {'reservations': filtered_reservations, 'clients': Clients, 'message': message, 'form': form},
            )
        
        else:
            return render(request,
            'website/waiting_reservations_list.html',
            {'reservations': filtered_reservations,'clients': Clients, 'message': message, 'form': form},
            )
    
    else:
        form = FiltersForm()
        all_reservations = Reservation.objects.filter(accepted='0')
        if len(all_reservations) == 0:
            message = "Aucune réservation à afficher."
        else:
            message = ""

        return render(request,
        'website/waiting_reservations_list.html',
        {'reservations': all_reservations, 'clients': Clients, 'message': message, 'form': form},
        )


def accept_reservation(request, id):
    return render(request,
    'website/accept_reservation.html',
    {'id': id},
    )


def accept_reservation_confirmed(request, id):    

    resa = Reservation.objects.get(id=id)
    resa.accepted = '1'
    resa.save()

    nb_people = resa.nb_people
    name = resa.name
    date_form = resa.resa_date
    hour = Reservation.HOUR_TRAD[resa.hour] 
    phone_num = resa.phone_number
    mail = resa.mail

    html_content = render_to_string("website/mails/accept_reservation_mail.html",
                {'nb_people': nb_people,
                'name': name,
                'date_form': translate_date(date_form),
                'hour': hour,
                'phone_number': phone_num,
                },
                )

    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject='[Restaurant L\'Air de Famille - Toulouse] Confirmation de votre réservation',
        body=text_content,
        from_email= settings.EMAIL_HOST_USER,
        to=[mail],
    )

    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)

    return redirect('display-reservations-list')


def refuse_reservation(request, id):

    return render(request,
    'website/refuse_reservation.html',
    {'id': id},
    )


def refuse_reservation_confirmed(request, id):
    resa = Reservation.objects.get(id=id)
    resa.accepted = '2'
    resa.save()

    nb_people = resa.nb_people
    name = resa.name
    date_form = resa.resa_date
    hour = Reservation.HOUR_TRAD[resa.hour] 
    mail = resa.mail

    html_content = render_to_string("website/mails/refuse_reservation_mail.html",
                {'nb_people': nb_people,
                'name': name,
                'date_form': translate_date(date_form),
                'hour': hour}
                )

    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject='[Restaurant L\'Air de Famille - Toulouse]  Récusation de votre réservation',
        body=text_content,
        from_email= settings.EMAIL_HOST_USER,
        to=[mail],
    )

    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)

    return redirect('display-reservations-list')


def display_accepted_reservations(request):
    reservations = Reservation.objects.filter(accepted='1')

    if len(reservations) == 0:
        message = "Aucune réservation à afficher."
    else:
        message = ""

    return render(request,
    'website/accepted_reservations_list.html',
    {'reservations': reservations, 'message': message},
    )


def display_refused_reservations(request):
    reservations = Reservation.objects.filter(accepted='2')

    if len(reservations) == 0:
        message = "Aucune réservation à afficher."
    else:
        message = ""

    return render(request,
    'website/refused_reservations_list.html',
    {'reservations': reservations, 'message': message},
    )


def display_reservation_details(request, id):
    resa = Reservation.objects.get(id=id)
    client = Client.objects.get(phone_number=resa.phone_number)

    return render(request,
    'website/reservation_details.html',
    {'reservation': resa, 'client': client},
    )


def edit_client(request, id):
    client = Client.objects.get(id=id)
    
    initial_data = {
        'comment': client.comment,
        'warning': client.warning,
    }

    if request.method == 'POST':
        
        form = EditClientForm(request.POST)
        
        if form.is_valid():
            new_comment = form.cleaned_data['comment']
            new_warning = form.cleaned_data['warning']
            client = Client.objects.get(id=id)
            client.comment = new_comment
            client.warning = new_warning
            client.save()

            return redirect('display-reservations-list')
        
        else:
            return render(request,
            'website/edit_client.html',
            {'client': client, 'form': form},
            )

    else:
        form = EditClientForm(initial=initial_data)

        return render(request,
        'website/edit_client.html',
        {'client': client, 'form': form},
        )


def display_clients_list(request):
    clients = Client.objects.all()

    return render(request,
    'website/clients_list.html',
    {'clients': clients},
    )


def display_client_details(request, id):
    client = Client.objects.get(id=id)

    return render(request,
    'website/client_details.html',
    {'client': client},
    )


def display_holidays(request):
    holidays = Holidays.objects.all()
    no_holidays_msg = "Aucune vacance de prévu."

    if len(holidays) == 0:
        return render(request,
        'website/display_holidays.html',
        {'holidays': holidays, 'message': no_holidays_msg},
        )
    
    else:
        return render(request,
        'website/display_holidays.html',
        {'holidays': holidays, 'message': ""},
        )


def add_holidays(request):


    past_date_msg = "Désolé, la date entrée est déjà passée."
    incoherent_date_msg = "Désolé, les dates entrées sont incohérentes entre elles."

    if request.method == 'POST':
        form = HolidaysForm(request.POST)

        if form.is_valid():
            if date_is_past(form.cleaned_data['begin']) or date_is_past(form.cleaned_data['end']):
                return render(request,
                'website/add_holidays.html',
                {'form': form, 'message': past_date_msg},
                )

            elif form.cleaned_data['begin'] >= form.cleaned_data['end']:
                return render(request,
                'website/add_holidays.html',
                {'form': form, 'message': incoherent_date_msg},
                )

            else:
                form.save()
                return redirect('display-holidays')
        
        else:
            return render(request,
            'website/add_holidays.html',
            {'form': form, 'message': "erreur"},
            )

    else:
        form = HolidaysForm

        return render(request,
        'website/add_holidays.html',
        {'form': form, 'message': ''},
        )


def delete_holidays(request, id):
    return render(request,
    'website/delete_holidays.html',
    {'id': id},
    )


def delete_holidays_confirmed(request, id):
    holidays = Holidays.objects.get(id=id)
    holidays.delete()

    return redirect('display-holidays')


def display_full_services(request):
    services = FullService.objects.all()

    if len(services) == 0:
        message = "Aucun service complet à afficher"
    else:
        message = ""

    return render(request,
    'website/display_full_services.html',
    {'services': services, 'message': message},
    )


def service_is_valid(date_form, meal_type, diner_closed_days):
    past_date_msg = "La date entrée est déjà passée."
    unexisting_date_msg = "Désolé, la date n'existe pas."
    bad_day_msg = "Désolé, la date tombe un lundi ou un dimanche."
    bad_evening_msg = "Désolé, le service entré correspond à un mardi ou un mercredi soir."

    try:                                                # on en tire le jour de la semaine correspondant                                 
        week_day = date_form.weekday()    
    except ValueError:                                          # si il y a une erreur alors date invalide, message d'erreur
        return unexisting_date_msg

    if date_is_past(date_form):
        return past_date_msg
            
    elif day_is_monday_or_sunday(week_day):
        return bad_day_msg

    elif reservation_on_unexisting_evening(meal_type, week_day, diner_closed_days):
        return bad_evening_msg

    else:
        return True



def add_full_service(request):

    if request.method == 'POST':
        form = FullServiceForm(request.POST)

        if form.is_valid():
            
            date_form = form.cleaned_data['date']
            meal_type = form.cleaned_data['meal_type']

            diner_closed_days = [1, 2]

            valid_return = service_is_valid(date_form, meal_type, diner_closed_days)

            if valid_return == True:
                form.save()

                return redirect('display-full-services')

            else:
                return render(request,
                'website/add_full_service.html',
                {'form': form, 'message': valid_return},
                )

        else:

            return render(request,
            'website/add_full_service',
            {'form': form, 'message': ""},
            )

    else:
        form = FullServiceForm()

        return render(request,
        'website/add_full_service.html',
        {'form': form, 'message': ""},
        )