from django.urls    import path

from bookings.views import BookingView

urlpatterns = [
    path('', BookingView.as_view())
]