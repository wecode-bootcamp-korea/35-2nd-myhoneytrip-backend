from django.urls import path, include

urlpatterns = [
    path('users', include('users.urls')),
    path('flights', include('flights.urls')),
    path('bookings', include('bookings.urls'))
]