from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProfileEditForm, FlightReservationForm, FlightForm
from .utils import filter_flights
from .models import Flight, FlightReservation

PAGES = 10


class IndexView(ListView):
    model = Flight
    template_name = 'flights/index.html'
    paginate_by = PAGES

    def get_queryset(self):
        flights = Flight.objects.select_related(
            'destination_airport',
            'departure_airport',
            'vehicle'
        )
        return filter_flights(flights)


class FlightDetailView(ListView):
    model = FlightReservation
    template_name = 'flights/flight_detail.html'
    paginate_by = PAGES

    def get_queryset(self):
        flight = get_object_or_404(
            Flight,
            id=self.kwargs['flight_id'],
        )

        self.extra_context = {'flight': flight}
        return flight.reservations.select_related('flight')


@login_required
def reserve_flight(request, flight_id):
    flight = get_object_or_404(
        Flight,
        id=flight_id,
    )
    if flight.reservations.count() >= flight.vehicle.capacity:
        return render(
            request,
            'flights/reservation_error.html',
            {'error': 'Мест нет'}
        )
    
    if flight.status != 'open':
        return render(
            request,
            'flights/reservation_error.html',
            {'error': 'Регистрация закрыта'},
        )
    
    form = FlightReservationForm(request.POST or None)
    if form.is_valid():
        reservation = form.save(commit=False)
        reservation.flight = flight
        reservation.save()
        return redirect(
            'flights:flight_detail',
            flight_id=flight.id
        )
    
    context = {'form': form, 'flight': flight}
    return render(
        request,
        'flights/flight_reservation.html',
        context
    )


@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(
        FlightReservation,
        id=reservation_id
    )
    form = FlightReservationForm(
        request.POST or None,
        instance=reservation
    )
    if form.is_valid():
        form.save()
        return redirect(
            'flights:flight_detail',
            flight_id=reservation.flight.id
        )

    context = {'form': form, 'reservation': reservation}
    return render(
        request,
        'flights/edit_reservation.html',
        context
    )


@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(
        FlightReservation,
        id=reservation_id
    )
    flight_id = reservation.flight.id
    if request.method == 'POST':
        reservation.delete()
        return redirect(
            'flights:flight_detail',
            flight_id=flight_id
        )
    context = {'reservation': reservation}
    return render(
        request,
        'flights/delete_reservation.html',
        context
    )


@login_required
def edit_flight(request, flight_id):
    flight = get_object_or_404(
        Flight,
        id=flight_id
    )
    form = FlightForm(
        request.POST or None,
        instance=flight
    )
    if form.is_valid():
        form.save()
        return redirect(
            'flights:flight_detail',
            flight_id=flight_id
        )
    
    context = {'form': form, 'flight': flight}
    return render(
        request,
        'flights/edit_flight.html',
        context
    )
    

@login_required
def create_flight(request):
    form = FlightForm(request.POST or None)
    if form.is_valid():
        flight = form.save(commit=False)
        flight.is_published = True
        flight.save()
        return redirect(
            'flights:flight_detail',
            flight_id=flight.id
        )

    context = {'form': form}
    return render(
        request,
        'flights/create_flight.html',
        context
    )


class RegisterView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('flights:index')


class ProfileView(DetailView):
    model = User
    template_name = "flights/profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs["username"])


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "flights/edit_profile.html"
    form_class = ProfileEditForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            "flights:profile", kwargs={"username": self.request.user.username}
        )
