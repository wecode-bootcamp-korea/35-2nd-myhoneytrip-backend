from django.urls import path

from bookings.views import MyBookingListView

urlpatterns = [
    path('/mytrip',MyBookingListView.as_view())
]
