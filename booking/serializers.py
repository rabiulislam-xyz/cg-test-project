from django.utils import timezone
from rest_framework import serializers

from booking.models import Vacancy, Booking, BookingStatus
from booking.utils import calculate_booking_amount
from booking.validators import has_booked_dates


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ('id', 'title', 'description', 'price')


class BookingSerializer(serializers.ModelSerializer):
    booked_dates = serializers.ReadOnlyField()
    booked_dates_count = serializers.ReadOnlyField()

    class Meta:
        model = Booking
        fields = ('id', 'vacancy', 'user', 'start_date', 'end_date',
                  'status', 'amount', 'booked_dates_count', 'booked_dates')
        read_only_fields = ('id', 'user', 'amount', 'status')

    def validate(self, data):
        if data['start_date'] < timezone.now().date():
            raise serializers.ValidationError('Booking date cannot be in the past')

        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('Start date must be before or same to end date')

        if has_booked_dates(data['start_date'], data['end_date']):
            raise serializers.ValidationError('There is already booked date/s in provided date range')

        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['vacancy'] = VacancySerializer(instance.vacancy).data
        return representation

    def create(self, validated_data):
        price = validated_data['vacancy'].price
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        validated_data['amount'] = calculate_booking_amount(price, start_date, end_date)
        validated_data['status'] = BookingStatus.CONFIRMED  # todo: make it dynamic based on payment status
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
