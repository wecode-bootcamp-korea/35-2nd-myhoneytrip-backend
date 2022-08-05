import json

from django.http     import JsonResponse
from django.views    import View

from bookings.models import Booking, BookingStatus, Ticket
from core.utils      import check_access, LocationNameEnum

class MyBookingListView(View):
    # @check_access
    def get(self, request):
        try:
            # user = request.user
            status_id = request.GET.get('status', 'upcoming')

            # status_set = {
            #     'upcoming' : 1,
            #     'last'     : 2,
            #     'canceled' : 3,
            # }
            status = BookingStatus.objects.get(id=status_id)

            bookings = Booking.objects.select_related('booking_status')\
                .prefetch_related('passenger_set','ticket_set','ticket_set__flight_detail','ticket_set__flight_detail__flight_route','ticket_set__flight_detail__flight_route__departure','ticket_set__flight_detail__flight_route__destination','ticket_set__flight_detail__flight_route__airplane__airline').filter(user_id = 1, booking_status_id = status.id)

            # if booking.passenger_set.all()[0].ticket_set.all().count() > 1:
            #     departure_info = {
            #         'departure_detail_id'   : booking.passenger_set.all()[0].ticket_set.all().get(flight_detail__flight_route__departure__name='Seoul').flight_detail.id,
            #         'destination_detail_id' : booking.passenger_set.all()[0].ticket_set.all().get(flight_detail__flight_route__destination__name='Seoul').flight_detail.id,
            #         'departure_time'        : booking.passenger_set.all()[0].ticket_set.all().get(flight_detail__flight_route__departure__name='Seoul').flight_detail.departure_time,
            #         'return_time'           : booking.passenger_set.all()[0].ticket_set.all().get(flight_detail__flight_route__destination__name='Seoul').flight_detail.arrival_time
            #     }
            # else:
            #     departure_info = {
            #         'flight_detail_id'      : booking.passenger_set.all()[0].ticket_set.all()[0].flight_detail.id,
            #         'departure_time'        : booking.passenger_set.all()[0].ticket_set.all()[0].flight_detail.departure_time,
            #         'return_time'           : booking.passenger_set.all()[0].ticket_set.all()[0].flight_detail.arrival_time
            #     }

            result = [({
                'round_trip'                      : {
                    'departure_info'              : {
                        'departure_detail_id'     : booking.passenger_set.all()[0].ticket_set.all().get(flight_detail__flight_route__departure__name='Seoul').flight_detail.id,
                        'departure_name'          : booking.passenger_set.all()[0].ticket_set.all().get(flight_detail__flight_route__departure__name='Seoul').flight_detail.flight_route.departure.korean_name,
                        'departure_time'          : booking.passenger_set.all()[0].ticket_set.all().get(flight_detail__flight_route__departure__name='Seoul').flight_detail.departure_time,
                        'departure_ticket_status' : booking.passenger_set.all()[0].ticket_set.all().get(flight_detail__flight_route__departure__name='Seoul').ticket_status.name,
                        'departure_airline_name'  : booking.passenger_set.all()[0].ticket_set.all().get(flight_detail__flight_route__departure__name='Seoul').flight_detail.flight_route.airplane.airline.name,
                        'departure_airline_logo'  : booking.passenger_set.all()[0].ticket_set.all().get(flight_detail__flight_route__departure__name='Seoul').flight_detail.flight_route.airplane.airline.logo_url,
                        },
                    'destination_info'              : {
                        'destination_detail_id'     : booking.passenger_set.all()[0].ticket_set.all().get(flight_detail__flight_route__destination__name='Seoul').flight_detail.id,
                        'destination_name'          : booking.passenger_set.all()[0].ticket_set.all().get(flight_detail__flight_route__destination__name='Seoul').flight_detail.flight_route.departure.korean_name,
                        'return_time'               : booking.passenger_set.all()[0].ticket_set.all().get(flight_detail__flight_route__destination__name='Seoul').flight_detail.arrival_time,
                        'destination_ticket_status' : booking.passenger_set.all()[0].ticket_set.all().get(flight_detail__flight_route__destination__name='Seoul').ticket_status.name,
                        'destination_airline_name'  : booking.passenger_set.all()[0].ticket_set.all().get(flight_detail__flight_route__destination__name='Seoul').flight_detail.flight_route.airplane.airline.name,
                        'destination_airline_logo'  : booking.passenger_set.all()[0].ticket_set.all().get(flight_detail__flight_route__destination__name='Seoul').flight_detail.flight_route.airplane.airline.logo_url,
                        },
                    'booking_info'       : {
                        'booking_id'     : booking.id,
                        'booking_number' : booking.booking_number,
                        'booking_status' : booking.booking_status.name,
                        }
                }} if booking.passenger_set.all()[0].ticket_set.all().count() > 1 else {
                'one_way'                         : {
                    'departure_info'              : {
                        'departure_detail_id'     : booking.passenger_set.all()[0].ticket_set.all()[0].flight_detail.id,
                        'departure_name'          : booking.passenger_set.all()[0].ticket_set.all()[0].flight_detail.flight_route.departure.korean_name,
                        'destination_name'        : booking.passenger_set.all()[0].ticket_set.all()[0].flight_detail.flight_route.destination.korean_name,
                        'departure_time'          : booking.passenger_set.all()[0].ticket_set.all()[0].flight_detail.departure_time,
                        'return_time'             : booking.passenger_set.all()[0].ticket_set.all()[0].flight_detail.arrival_time,
                        'departure_ticket_status' : booking.passenger_set.all()[0].ticket_set.all()[0].ticket_status.name,
                        'airline_name'            : booking.passenger_set.all()[0].ticket_set.all()[0].flight_detail.flight_route.airplane.airline.name,
                        'airline_logo'            : booking.passenger_set.all()[0].ticket_set.all()[0].flight_detail.flight_route.airplane.airline.logo_url
                        },
                    
                    'booking_info'        : {
                        'booking_id'      : booking.id,
                        'booking_number'  : booking.booking_number,
                        'booking_status'  : booking.booking_status.name,
                        }
                        }})for booking in bookings]

            # result = [{
            #     'departure_detail'       : {
            #         'flight_detail_id'   : booking.ticket_set.all()[0].flight_detail.id,
            #         'flight_detail_time' : booking.ticket_set.all()[0].flight_detail.departure_time,
            #     },
            #     'destination_detail'     : {
            #         'flight_detail_id'   : booking.ticket_set.all()[0].flight_detail.id,
            #         'flight_detail_time' : booking.ticket_set.all()[0].flight_detail.arrival_time,
            #     },
            #     'booking'                : {
            #         'booking_id'         : booking.id,
            #         'booking_number'     : booking.booking_number,
            #         'booking_status'     : booking.booking_status.name
            #     },
            #     'airline'                : {
            #         'airline_id'         : booking.ticket_set.all()[0].flight_detail.flight_route.airplane.airline.id,
            #         'airline_name'       : booking.ticket_set.all()[0].flight_detail.flight_route.airplane.airline.name,
            #         'airline_logo'       : booking.ticket_set.all()[0].flight_detail.flight_route.airplane.airline.logo_url,
            #     },
            #     'departure'              : {
            #         'departure_id'       : booking.ticket_set.all()[0].flight_detail.flight_route.departure.id,
            #         'departure_name'     : booking.ticket_set.all()[0].flight_detail.flight_route.departure.korean_name,
            #     },
            #     'destination'            : {
            #         'destination_id'     : booking.ticket_set.all()[0].flight_detail.flight_route.destination.id,
            #         'destination_name'   : booking.ticket_set.all()[0].flight_detail.flight_route.destination.korean_name,
            #     },
            #     'ticket'                 : {
            #         'ticket_status'      : booking.ticket_set.all()[0].ticket_status.name
            #     }
            # } for booking in bookings]

            return JsonResponse({'result':result}, status=200)
        except BookingStatus.DoesNotExist:
            return JsonResponse({'MESSAGE': 'Booking status matching query does not exist.'}, status = 404)