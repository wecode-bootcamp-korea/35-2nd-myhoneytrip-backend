import json
from uuid            import uuid4
from operator        import attrgetter

from django.db       import transaction
from django.http     import JsonResponse
from django.views    import View
from django.db.models import Min, Max

from bookings.models import (
    Booking,
    BookingStatus,
    Passenger,
    Ticket,
    TicketStatus
    )
from core.utils      import (
    BookingStatusEnum,
    TicketStatusEnum,
    check_access,
    BookingStatusEnum,
    TicketStatusEnum
    )
from flights.models  import FlightDetail

class BookingView(View):
    @check_access
    def post(self, request):
        try:
            with transaction.atomic():
                data = json.loads(request.body)
                user = request.user

                passengers     = data['passengers']
                flight_details = data['flight_detail_id']

                upcoming       = BookingStatusEnum.UPCOMING.value
                ticket_confirm = TicketStatusEnum.CONFIRM.value
         
                booking = Booking.objects.create(
                    booker_name          = data['booker_name'],
                    booker_email         = data['booker_email'],
                    booker_mobile_number = data['booker_mobile_number'],
                    booking_status       = BookingStatus.objects.get(id = upcoming),
                    user                 = user.id,
                    booking_number       = uuid4()
                )

                passenger_list = [Passenger(
                    first_name = passenger['first_name'],
                    last_name  = passenger['last_name'],
                    gender     = passenger['gender'],
                    birthday   = passenger['birthday'],
                    booking_id = booking.id)
                for passenger in passengers]

                Passenger.objects.bulk_create(passenger_list)

                [Ticket.objects.create(
                    tichet_number = uuid4(),
                    passenger_id  = passenger.id,
                    booking_id    = booking.id,
                    ticket_status_id = TicketStatus.objects.get(id = ticket_confirm),
                    flight_detail = FlightDetail.objects.get(id = detail))
                for passenger in passenger_list for detail in flight_details]

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except FlightDetail.DoesNotExist:
            return JsonResponse({'message' : 'FLIGHT_DETAIL KEY_ERROR'}, status = 404)


class MyBookingListView(View):
    @check_access
    def get(self, request):
        try:
            user       = request.user
            status_id  = request.GET.get('status', 'upcoming')

            status_set = {
                'upcoming' : BookingStatusEnum.UPCOMING.value,
                'last'     : BookingStatusEnum.LAST.value,
                'canceled' : BookingStatusEnum.CANCELED.value,
            }

            status_id = status_id if status_id in status_set.keys() else 'upcoming'

            bookings = Booking.objects.select_related('booking_status')\
                .annotate(min_departure_time=Min('ticket__flight_detail__departure_time'), max_departure_time=Max('ticket__flight_detail__departure_time'))\
                .filter(user = user, booking_status_id = status_set.get(status_id))
                
            booking_list = []


            for booking in bookings:
                booking_list.append(booking)
                if booking.min_departure_time != booking.max_departure_time:
                    booking_return                    = bookings.annotate(min_departure_time=Min('ticket__flight_detail__departure_time'), max_departure_time=Max('ticket__flight_detail__departure_time')).get(id = booking.id)
                    booking_return.min_departure_time = booking_return.max_departure_time
                    booking_list.append(booking_return)

            booking_list.sort(key = attrgetter('min_departure_time'))

            flight_detail = FlightDetail.objects.all().select_related('flight_route__airplane__airline', 'flight_route__departure', 'flight_route__destination')

            result = [{
                'booking_id'       : booking.id,
                'booking_number'   : booking.booking_number,
                'booking_status'   : booking.booking_status.name,
                'departure_name'   : flight_detail.filter(ticket__booking__id=booking.id, departure_time = booking.min_departure_time).first().flight_route.departure.korean_name,
                'departure_date'   : booking.min_departure_time,
                'arrival_name'     : flight_detail.filter(ticket__booking__id=booking.id, departure_time = booking.min_departure_time).first().flight_route.destination.korean_name,
                'arrival_date'     : flight_detail.filter(ticket__booking__id=booking.id, departure_time = booking.min_departure_time).first().arrival_time,
                'airline'  : {
                    'id'   : flight_detail.filter(ticket__booking__id=booking.id).first().flight_route.airplane.airline.id,
                    'name' : flight_detail.filter(ticket__booking__id=booking.id).first().flight_route.airplane.airline.name,
                    'logo' : flight_detail.filter(ticket__booking__id=booking.id).first().flight_route.airplane.airline.logo_url,
                }
            }for booking in booking_list]

            return JsonResponse({'result': result}, status=200)
        except BookingStatus.DoesNotExist:
            return JsonResponse({'MESSAGE': 'Booking status matching query does not exist.'}, status = 404)
    
    @check_access
    def patch(self, request):
        try:
            user           = request.user
            data           = json.loads(request.body)
            booking_id     = data['booking_id']
            booking_status = BookingStatusEnum.CANCELED.value
            ticket_status  = TicketStatusEnum.CANCELED.value

            booking = Booking.objects.filter(id = booking_id, user= user)
            ticket  = Ticket.objects.filter(booking_id = booking_id)
            
            if not booking:
                return JsonResponse({'message': 'Booking matching query does not exist.'}, status = 404)
            if not ticket:
                return JsonResponse({'message': 'Ticket matching query does not exist.'}, status = 404)
            
            booking.update(booking_status_id = booking_status)        
            ticket.update(ticket_status_id = ticket_status)

            return JsonResponse({'message' : 'CANCEL SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
