from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from booking.models import BookingStatus, Booking, Vacancy
from booking.serializers import VacancySerializer, BookingSerializer
from project.permissions import IsOwn


class VacancyViewSet(viewsets.ModelViewSet):
    serializer_class = VacancySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    queryset = Vacancy.objects.all()


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.select_related('vacancy', 'user').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['note']
    ordering_fields = ['start_date', 'end_date']
    filterset_fields = {
        'start_date': ['gte', 'lte', 'exact', 'gt', 'lt'],
        'end_date': ['gte', 'lte', 'exact', 'gt', 'lt']
    }

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated, IsOwn]
        return super().get_permissions()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
