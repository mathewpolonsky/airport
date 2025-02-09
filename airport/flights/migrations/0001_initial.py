# Generated by Django 3.2.16 on 2025-01-25 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')),
                ('name', models.CharField(max_length=256, verbose_name='Название аэропорта')),
                ('location', models.CharField(max_length=256, verbose_name='Местонахождение аэропорта')),
            ],
            options={
                'verbose_name': 'Аэропорт',
                'verbose_name_plural': 'Аэропорты',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')),
                ('number', models.CharField(max_length=256, verbose_name='Номер рейса')),
                ('departure_time', models.DateTimeField(verbose_name='Время вылета')),
                ('arrival_time', models.DateTimeField(verbose_name='Время прибытия')),
                ('status', models.CharField(choices=[('open', 'Регистрация открыта'), ('closed', 'Регистрация закрыта'), ('in_progress', 'В пути'), ('completed', 'Завершен')], default='open', max_length=64, verbose_name='Статус рейса')),
                ('departure_airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departures', to='flights.airport', verbose_name='Аэропорт отправления')),
                ('destination_airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrivals', to='flights.airport', verbose_name='Аэропорт назначения')),
            ],
            options={
                'verbose_name': 'Рейс',
                'verbose_name_plural': 'Рейсы',
                'ordering': ('-departure_time',),
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')),
                ('model', models.CharField(max_length=256, verbose_name='Модель')),
                ('vehicle_type', models.CharField(choices=[('airplane', 'Самолет'), ('helicopter', 'Вертолет')], max_length=32, verbose_name='Тип транспорта')),
                ('capacity', models.PositiveIntegerField(verbose_name='Число посадочных мест')),
            ],
            options={
                'verbose_name': 'Транспорт',
                'verbose_name_plural': 'Транспорты',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='FlightReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')),
                ('seat_number', models.CharField(max_length=16, verbose_name='Номер места')),
                ('passenger_name', models.CharField(max_length=256, verbose_name='ФИО пассажира')),
                ('phone_number', models.CharField(max_length=16, verbose_name='Номер телефона пассажира')),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='flights.flight', verbose_name='Рейс')),
            ],
            options={
                'verbose_name': 'Бронь рейса',
                'verbose_name_plural': 'Брони рейса',
            },
        ),
        migrations.AddField(
            model_name='flight',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flights', to='flights.vehicle', verbose_name='Транспорт'),
        ),
    ]
