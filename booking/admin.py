from django.contrib import admin

from booking.models import Vacancy, Booking


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description']
    list_display = ['title', 'price']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'booked_dates_count', 'status', 'user', 'vacancy']
    list_filter = ['status']
