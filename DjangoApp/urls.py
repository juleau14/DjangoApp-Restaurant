"""DjangoApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from website import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.redirect_home, name='redirect-home'),

    path('close_tab', views.close_tab, name='close-tab'),
    
    path('home/', views.home, name='home'),

    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    
    path('reservation/', views.make_reservation, name='reservation-page'),
    path('reservation/confirmation/<str:mail>/', views.reservation_confirmated, name='confirmation-page'),
    
    path('manage_reservations/<str:url_date>/<str:url_meal>/', views.display_reservations_list, name='display-reservations-list'),
    path('manage_reservations/infos/<int:id>/details/', views.display_reservation_details, name='display-details'),
    
    path('manage_reservations/treat/<int:id>/accept/', views.accept_reservation, name='accept-reservation'),
    path('manage_reservations/treat/<int:id>/accept/confirmed/', views.accept_reservation_confirmed, name='accept-reservation-confirmed'),
    
    path('manage_reservations/treat/<int:id>/refuse/', views.refuse_reservation, name='refuse-reservation'),
    path('manage_reservations/treat/<int:id>/refuse/confirmed/', views.refuse_reservation_confirmed, name='refuse-reservation-confirmed'),
    
    path('manage_reservations/accepted_reservations/', views.display_accepted_reservations, name='accepted-reservations'),
    path('manage_reservations/refused_reservations/', views.display_refused_reservations, name='refused-reservations'),
    
    path('manage_mails/mail_errors/', views.display_mail_errors, name='mail-errors'),
    path('manage_mails/treat_mail_error/<int:id>/', views.treat_mail_error, name='treat-mail-error'),
    path('manage_mails/treat_mail_error/<int:id>/solved/', views.mail_error_solved, name='mail-error-solved'),
    path('manage_mails/old_mail_errors/', views.display_old_mail_errors, name='old-mail-errors'),
    path('manage_mails/model/<int:id>/', views.model_error_mail, name='model-error-mail'),

    path('manage_clients/', views.display_clients_list, name='clients-list'),
    path('manage_clients/<int:id>/details/', views.display_client_details, name='display-client-details'),
    path('manage_clients/<int:id>/edit/', views.edit_client, name='edit-client'),

    path('holidays/', views.display_holidays, name='display-holidays'),
    path('holidays/add/', views.add_holidays, name='add-holidays'),
    path('holidays/delete/<int:id>/', views.delete_holidays, name='delete-holidays'),
    path('holidays/delete/<int:id>/confirmed/', views.delete_holidays_confirmed, name='delete-holidays-confirmed'),

    path('full_services/', views.display_full_services, name='display-full-services'),
    path('full_services/add/', views.add_full_service, name='add-full-service'),

    path('reservation/maintenance', views.maintenance, name='maintenance'),
]
