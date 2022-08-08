from django.urls import path

from flights.views import FlightListView

urlpatterns = [
    path('', FlightListView.as_view())
]