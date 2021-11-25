from datetime import date
from typing import List

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from booking.utils import days_count as days_count_util
from booking.utils import date_list as date_list_util

User = get_user_model()


class Vacancy(models.Model):
    title = models.CharField(
        max_length=150)

    description = models.TextField(
        blank=True,
        null=True)

    price = models.FloatField()

    created_at = models.DateTimeField(
        auto_now_add=True)

    updated_at = models.DateTimeField(
        auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Vacancies'
        ordering = ['-created_at']


class BookingStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    CONFIRMED = 'CONFIRMED', _('Confirmed')
    CANCELED = 'CANCELED', _('Canceled')


class Booking(models.Model):
    user = models.ForeignKey(
        User,
        related_name='bookings',
        on_delete=models.PROTECT)

    vacancy = models.ForeignKey(
        Vacancy,
        related_name='bookings',
        on_delete=models.PROTECT)

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING)

    amount = models.FloatField(
        default=0)

    note = models.TextField(
        blank=True,
        null=True)

    created_at = models.DateTimeField(
        auto_now_add=True)

    updated_at = models.DateTimeField(
        auto_now=True)

    @property
    def booked_dates_count(self) -> int:
        return days_count_util(self.start_date, self.end_date)

    @property
    def booked_dates(self) -> List[date]:
        return date_list_util(self.start_date, self.booked_dates_count)

    def __str__(self):
        if self.start_date == self.end_date:
            return f'Booking of {self.start_date}'
        return f'Booking from {self.start_date} to {self.end_date}'

    class Meta:
        ordering = ['-created_at']
