from django.urls    import path

from bookings.views import ReservationView

urlpatterns = [
    path('/reservation', ReservationView.as_view())
]