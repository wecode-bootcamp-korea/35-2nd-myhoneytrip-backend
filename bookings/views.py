import json
from uuid import uuid4

from django.db       import transaction
from django.http     import JsonResponse
from django.views    import View

from core.utils      import check_access, BookingStatusEnum, TicketStatusEnum
from flights.models  import FlightDetail
from bookings.models import (
    Booking, 
    BookingStatus, 
    Passenger, 
    Ticket, 
)

class ReservationView(View):
    @check_access
    def post(self, request):
        try:
            with transaction.atomic():
                data = json.loads(request.body)
                user = request.user

                passengers     = data['passengers']
                flight_details = data['flight_detail_id'] #[1], [1,2]
                
                upcoming       =  BookingStatusEnum.UPCOMING.value
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
                    booking_id = booking.id
                )for passenger in passengers]

                Passenger.objects.bulk_create(passenger_list)

                [Ticket.objects.create(
                    tichet_number    = uuid4(),
                    passenger_id     = passenger.id,
                    booking_id       = booking.id,
                    ticket_status_id = ticket_confirm,
                    flight_detail    = FlightDetail.objects.get(id = detail)
                )for passenger in passenger_list for detail in flight_details]

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEYERROR'}, status = 400)