from django.db   import models

from core.models import TimeStampModel

class Booking(TimeStampModel): 
    booking_number       = models.UUIDField()
    booker_name          = models.CharField(max_length=50)
    booker_email         = models.CharField(max_length=200)
    booker_mobile_number = models.CharField(max_length=20)
    booking_status       = models.ForeignKey('BookingStatus', on_delete = models.CASCADE)
    user                 = models.ForeignKey('users.User', on_delete = models.CASCADE)

    class Meta: 
        db_table = 'bookings'


class BookingStatus(models.Model): 
    name = models.CharField(max_length=50)

    class Meta: 
        db_table = 'booking_statuses'


class Passenger(TimeStampModel): 
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    gender     = models.CharField(max_length=10)
    birthday   = models.DateField()
    booking    = models.ForeignKey('Booking', on_delete = models.CASCADE)

    class Meta: 
        db_table = 'passengers'


class Ticket(TimeStampModel): 
    tichet_number = models.UUIDField()
    passenger     = models.ForeignKey('Passenger', on_delete = models.CASCADE)
    booking       = models.ForeignKey('Booking', on_delete = models.CASCADE)
    ticket_status = models.ForeignKey('TicketStatus', on_delete = models.CASCADE)
    flight_detail = models.ForeignKey('flights.FlightDetail', on_delete = models.CASCADE)

    class Meta: 
        db_table = 'tickets'


class TicketStatus(models.Model): 
    name = models.CharField(max_length=50)

    class Meta: 
        db_table = 'ticket_statuses'