from django.urls import path,include

urlpatterns = [
    path('bookings', include('bookings.urls'))
]
