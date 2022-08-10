import json

from django.http     import JsonResponse
from django.views    import View

from bookings.models import Booking, BookingStatus, Ticket
from core.utils      import check_access, LocationNameEnum

class MyBookingListView(View):
    """
    목적: 내가 예약한 예약 목록

    조건
        - 비행기 출발 순으로 정렬
        - 같은 예약의 왕복 여정도 날짜 순으로 표시
    
    """
    
    
    
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
                .prefetch_related('passenger_set','ticket_set','ticket_set__flight_detail','ticket_set__flight_detail__flight_route','ticket_set__flight_detail__flight_route__departure','ticket_set__flight_detail__flight_route__destination','ticket_set__flight_detail__flight_route__airplane__airline')\
                .annotate()\
                .filter(user_id = 1, booking_status_id = status.id)

            """
            불러온 query_set annotate한 시간 비교해서 왕복이면 객체 하나 더 추가
            추가가 완료된 list 시간 순으로 정렬(operator 모듈 이용)
            """
            
            result = [{
                "booking_id" : 
                "booking_number" :
                "booking_status" :
                "departure_name" : FlightDetail.objects.filter(ticket__booking__id=book.id).first().flight_route.departure.korean_name
                "departure_date" : b
                "departure_day" :
                "arrival_name" :
                "arrival_date" :
                "arrival_day" :
                "airline" : {
                    "airline_id" : 
                    'name'       : 
                    'logo'       : 
                },
            }

            }for book in bookings]

            return JsonResponse({'result':result}, status=200)
        except BookingStatus.DoesNotExist:
            return JsonResponse({'MESSAGE': 'Booking status matching query does not exist.'}, status = 404)