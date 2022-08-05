from django.urls    import path

from bookings.views import BookingView, MyBookingListView

urlpatterns = [
    path('', BookingView.as_view()),
    path('/mytrip',MyBookingListView.as_view())
]
