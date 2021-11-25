from django.db.models import Q

from booking.models import Booking


def has_booked_dates(start_date, end_date) -> bool:
    """
    Check if there is already any booking in the given dates

    Try to find bookings that available in provided date range,
    or find bookings that contains either provided start date or end date
    """
    return Booking.objects.filter(
        Q(start_date__lte=end_date, end_date__gte=start_date) |
        Q(start_date__lte=start_date, end_date__gte=start_date) |
        Q(start_date__lte=end_date, end_date__gte=end_date)
    ).exists()
