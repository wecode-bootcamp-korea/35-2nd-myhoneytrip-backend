from django.views     import View
from django.http      import JsonResponse

from flights.models   import FlightDetail

class FlightListView(View):
    def get(self, request):
        try:
            data             = request.GET
            departure_name   = data['departure_name']
            destination_name = data['destination_name']
            departure_date   = data['departure_date']
            return_date      = request.GET.get('return_date', 0)
            passengers       = data['passenger']
            airlines         = request.GET.getlist('airline', ['HoneyAirline', 'MoonAirline'])
            sort_type        = request.GET.get('sort_by','lowest_fare')
            offset           = int(request.GET.get('offset', 0))
            limit            = int(request.GET.get('limit', 5))

            sort_options = {
                'lowest_fare' : 'price',
                'fastest_time': 'departure_time'
            }

            departure_options = FlightDetail.objects.select_related('flight_route') \
                                .filter(departure_time__day=departure_date, \
                                        flight_route__departure__name=departure_name, \
                                        flight_route__destination__name=destination_name, \
                                        remaining_seats__gte=passengers, \
                                        flight_route__airplane__airline__name__in=airlines).order_by(sort_options[sort_type])

            return_options = FlightDetail.objects.select_related('flight_route') \
                            .filter(departure_time__day=return_date, \
                                    flight_route__departure__name=destination_name, \
                                    flight_route__destination__name=departure_name, \
                                    remaining_seats__gte=passengers, 
                                    flight_route__airplane__airline__name__in=airlines).order_by(sort_options[sort_type])

            get_flight_time = lambda x : round(x.seconds/3600)

            departure_info = [{
                'flight_detail_id'           : departure_option.id,
                'flight_route_code'          : departure_option.flight_route.code,
                'departure_location'         : departure_option.flight_route.departure.name,
                'departure_location_korean'  : departure_option.flight_route.departure.korean_name,
                'departure_airport_code'     : departure_option.flight_route.departure.airport_code,
                'destination_location'       : departure_option.flight_route.destination.name,
                'destination_location_korean': departure_option.flight_route.destination.korean_name,
                'destination_airport_code'   : departure_option.flight_route.destination.airport_code,
                'month'                      : departure_option.departure_time.month,
                'date'                       : departure_option.departure_time.day,
                'day'                        : departure_option.departure_time.isoweekday(),
                'airline'                    : departure_option.flight_route.airplane.airline.name,
                'airline_url'                : departure_option.flight_route.airplane.airline.logo_url,
                'departure_time'             : departure_option.departure_time.strftime('%H:%M'),
                'arrival_time'               : departure_option.arrival_time.strftime('%H:%M'),
                'flight_time'                : get_flight_time(departure_option.departure_time-departure_option.arrival_time),
                'price'                      : departure_option.price,
                'remaining_seats'            : departure_option.remaining_seats,
                'passengers'                 : passengers
                } for departure_option in departure_options[offset:offset+limit]]

            return_info = [{
                'flight_detail_id'           : return_option.id,
                'flight_route_code'          : return_option.flight_route.code,
                'departure_location'         : return_option.flight_route.departure.name,
                'departure_location_korean'  : return_option.flight_route.departure.korean_name,
                'departure_airport_code'     : return_option.flight_route.departure.airport_code,
                'destination_location'       : return_option.flight_route.destination.name,
                'destination_location_korean': return_option.flight_route.destination.korean_name,
                'destination_airport_code'   : return_option.flight_route.destination.airport_code,
                'month'                      : return_option.departure_time.month,
                'date'                       : return_option.departure_time.day,
                'day'                        : return_option.departure_time.isoweekday(),
                'airline'                    : return_option.flight_route.airplane.airline.name,
                'airline_url'                : return_option.flight_route.airplane.airline.logo_url,
                'departure_time'             : return_option.departure_time.strftime('%H:%M'),
                'arrival_time'               : return_option.arrival_time.strftime('%H:%M'),
                'flight_time'                : get_flight_time(return_option.departure_time - return_option.arrival_time),
                'price'                      : return_option.price,
                'remaining_seats'            : return_option.remaining_seats,
                'passengers'                 : passengers
                } for return_option in return_options[offset:offset+limit]]

            return JsonResponse({'departure_list': departure_info,'return_list':return_info} , status=200)
                
        except KeyError:
            return JsonResponse({'message':'Key_Error'}, status=400)