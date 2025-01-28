from django.urls import path

from . import views


app_name = 'flights'


urlpatterns = [
     path('', views.IndexView.as_view(), name='index'),

     path('flight/<int:flight_id>/',
          views.FlightDetailView.as_view(),
          name='flight_detail'),
     path('flight/create/',
          views.create_flight,
          name='create_flight'),
     path('flight/<int:flight_id>/edit',
          views.edit_flight,
          name='edit_flight'),

     path('flight/<int:flight_id>/reserve/',
          views.reserve_flight,
          name='reserve_flight'),
     path('reservation/<int:reservation_id>/edit',
          views.edit_reservation,
          name='edit_reservation'),
     path('reservation/<int:reservation_id>/delete',
          views.delete_reservation,
          name='delete_reservation'),

     path('profile/edit/',
          views.EditProfileView.as_view(),
          name='edit_profile'),
     path('profile/<str:username>/',
          views.ProfileView.as_view(),
          name='profile')
]