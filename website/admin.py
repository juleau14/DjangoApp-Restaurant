from django.contrib import admin
from website.models import Reservation, Client, Holidays, FullService

class ReservationAdmin(admin.ModelAdmin):
	list_display = ('name', 'nb_people')

class ClientAdmin(admin.ModelAdmin):
	list_display = ('name', 'phone_number', 'nb_reservations')

class HolidaysAdmin(admin.ModelAdmin):
	list_display = ('begin', 'end')

class FullServiceAdmin(admin.ModelAdmin):
	list_display = ('date', 'meal_type')

admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Holidays, HolidaysAdmin)
admin.site.register(FullService, FullServiceAdmin)


