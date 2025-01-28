from .models import Flight


def filter_flights(flights):
    flights = flights.filter(
        is_published=True
    )
    return flights
