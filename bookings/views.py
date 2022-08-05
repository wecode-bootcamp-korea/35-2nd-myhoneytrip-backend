import json

from uuid            import uuid4

from django.db       import transaction
from django.http     import JsonResponse
from django.views    import View

from bookings.models import Booking, BookingStatus, Passenger, Ticket, TicketStatus
from core.utils      import check_access, Bookingstatus, Ticketstatus
from flights.models  import FlightDetail

class ReservationView(View):
    @check_access
    def post(self, request):
        try:
            with transaction.atomic():
                data    = json.loads(request.body)
                user = request.user

                passengers = data['passengers']
                details = data['flight_detail_id']
         
                booking = Booking.objects.create(
                    booker_name          = data['booker_name'],
                    booker_email         = data['booker_email'],
                    booker_mobile_number = data['booker_mobile_number'],
                    booking_status       = BookingStatus.objects.get(id = Bookingstatus.An_Upcoming_Trip.value),
                    user                 = user.id,
                    booking_number       = uuid4()
                )

                [Passenger.objects.create(
                    first_name = passenger['first_name'],
                    last_name  = passenger['last_name'],
                    gender     = passenger['gender'],
                    birthday   = passenger['birthday'],
                    booking_id = booking.id)for passenger in passengers]
                    
                ticket_passensgers = Passenger.objects.filter(booking_id = booking.id)

                [Ticket.objects.create(
                    tichet_number = uuid4(),
                    passenger_id  = passenger.id,
                    booking_id    = booking.id,
                    ticket_status = TicketStatus.objects.get(id = Ticketstatus.Confirm.value),
                    flight_detail = FlightDetail.objects.get(id = detail))for passenger in ticket_passensgers for detail in details]

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEYERROR'}, status = 400)