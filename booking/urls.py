from django.urls import path, include
from rest_framework import routers

from booking.views import VacancyViewSet, BookingViewSet

router = routers.DefaultRouter()
router.register(r'vacancies', VacancyViewSet, basename='vacancy')
router.register(r'bookings', BookingViewSet, basename='booking')


urlpatterns = [
    path('', include(router.urls)),
]
