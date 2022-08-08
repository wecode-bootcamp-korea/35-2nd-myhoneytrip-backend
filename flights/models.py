from django.db   import models

from core.models import TimeStampModel


class FlightDetail(TimeStampModel): 
    departure_time  = models.DateTimeField()
    arrival_time    = models.DateTimeField()
    remaining_seats = models.IntegerField()
    reserved_seats  = models.IntegerField()
    price           = models.DecimalField(max_digits=15, decimal_places=2)
    flight_route    = models.ForeignKey('FlightRoute', on_delete=models.CASCADE)

    class Meta: 
        db_table = 'flight_details'


class FlightRoute(TimeStampModel): 
    code        = models.CharField(max_length = 10)
    departure   = models.ForeignKey('Location', related_name = 'departure_flight_routes', on_delete = models.CASCADE)
    destination = models.ForeignKey('Location', related_name = 'destination_flight_routes', on_delete = models.CASCADE)
    airplane    = models.ForeignKey('Airplane', on_delete = models.CASCADE)

    class Meta: 
        db_table = 'flight_routes'


class Location(TimeStampModel): 
    name         = models.CharField(max_length = 50)
    korean_name  = models.CharField(max_length = 50)
    airport_code = models.CharField(max_length = 50)
    airport_name = models.CharField(max_length = 100)

    class Meta: 
        db_table = 'locations'


class LocationImage(models.Model): 
    location_url = models.CharField(max_length = 300)
    location     = models.ForeignKey('Location', on_delete = models.CASCADE)

    class Meta: 
        db_table = 'location_images'


class Airplane(TimeStampModel): 
    name            = models.CharField(max_length = 50)
    airplane_code   = models.CharField(max_length = 50)
    number_of_seats = models.IntegerField()
    airline         = models.ForeignKey('Airline', on_delete = models.CASCADE)

    class Meta: 
        db_table = 'airplane'


class Airline(models.Model): 
    name     = models.CharField(max_length = 50)
    logo_url = models.CharField(max_length = 300)

    class Meta: 
        db_table = 'airlines'