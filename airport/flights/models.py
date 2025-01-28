from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()
TEXT_LENGTH = 256


class TimestampModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class Airport(TimestampModel):
    name = models.CharField(
        max_length=TEXT_LENGTH,
        verbose_name='Название аэропорта'
    )
    location = models.CharField(
        max_length=TEXT_LENGTH,
        verbose_name='Местонахождение аэропорта'
    )

    class Meta:
        verbose_name = 'Аэропорт'
        verbose_name_plural = 'Аэропорты'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name


class Vehicle(TimestampModel):
    VEHICLE_TYPE_CHOICES = [
        ("airplane", "Самолет"),
        ("helicopter", "Вертолет"),
    ]
    model = models.CharField(
        max_length=TEXT_LENGTH,
        verbose_name='Модель'
    )
    vehicle_type = models.CharField(
        max_length=32,
        choices=VEHICLE_TYPE_CHOICES,
        verbose_name='Тип транспорта'
    )
    capacity = models.PositiveIntegerField(
        verbose_name='Число посадочных мест'
    )

    class Meta:
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспорты'
        ordering = ('-created_at',)
    
    def __str__(self):
        return f"{self.model} ({self.get_vehicle_type_display()})"


class Flight(TimestampModel):
    FLIGHT_STATUS_CHOICES = [
        ("open", "Регистрация открыта"),
        ("closed", "Регистрация закрыта"),
        ("in_progress", "В пути"),
        ("completed", "Завершен"),
    ]

    number = models.CharField(
        max_length=TEXT_LENGTH,
        verbose_name='Номер рейса'
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='flights',
        verbose_name='Транспорт'
    )
    destination_airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name='arrivals',
        verbose_name='Аэропорт назначения'
    )
    departure_airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name='departures',
        verbose_name='Аэропорт отправления'
    )
    departure_time = models.DateTimeField(
        verbose_name='Время вылета'
    )
    arrival_time = models.DateTimeField(
        verbose_name='Время прибытия'
    )
    status = models.CharField(
        choices=FLIGHT_STATUS_CHOICES,
        max_length=64,
        default='open',
        verbose_name='Статус рейса'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Отображено'
    )

    def get_status_display(self):
        return dict(self.FLIGHT_STATUS_CHOICES).get(self.status)
    
    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'
        ordering = ('departure_time',)

    def __str__(self):
        return self.number


class FlightReservation(TimestampModel):
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name='Рейс'
    )
    seat_number = models.CharField(
        max_length=16,
        verbose_name='Номер места'
    )
    passenger_name = models.CharField(
        max_length=TEXT_LENGTH,
        verbose_name='ФИО пассажира'
    )
    phone_number = models.CharField(
        max_length=16,
        verbose_name='Номер телефона пассажира'
    )

    class Meta:
        verbose_name = 'Бронь рейса'
        verbose_name_plural = 'Брони рейса'
        ordering = ('-created_at',)
    
    def __str__(self):
        return f"{self.passenger_name} - {self.seat_number}"
