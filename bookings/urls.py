from django.urls    import path

from bookings.views import BookingView, MyBookingListView, MyBookingView

urlpatterns = [
    path('', BookingView.as_view()),
    path('/mytrip',MyBookingListView.as_view()),
    path('/mytrip/<int:booking_id>',MyBookingView.as_view())
]
