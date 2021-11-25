from datetime import timedelta, date
from typing import List


def days_count(start_date: date, end_date: date) -> int:
    # from and to dates are inclusive, adding 1 to the difference
    return (end_date - start_date).days + 1


def date_list(start_date: date, days_range: int = 1) -> List[date]:
    """
    Returns a list of dates from start_date to start_date + days_range
    """
    return [
        start_date + timedelta(days=i)
        for i in range(days_range)
    ]


def calculate_booking_amount(vacancy_price: float, start_date: date, end_date: date) -> float:
    """
    Calculates the amount of the booking based on the price of the vacancy and the days
    """
    return vacancy_price * days_count(start_date, end_date)
