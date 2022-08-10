from django.test    import TestCase, Client

from flights.models import FlightDetail, FlightRoute, Airline, Location, Airplane

class FlightListViewTest(TestCase):
    def setUp(self):
        client = Client()

        hawaii = Location.objects.create(
            id           = 1,
            name         = 'Hawaii',
            korean_name  = '하와이',
            airport_code = 'HNL',
            airport_name = 'Honolulu'
        )

        seoul = Location.objects.create(
            id           = 2,
            name         = 'Seoul',
            korean_name  = '서울',
            airport_code = 'SEL',
            airport_name = 'Incheon'
        )

        Airline.objects.create(
            id       = 1,
            name     = 'HoneyAirline',
            logo_url = '1'
        )

        Airline.objects.create(
            id       = 2,
            name     = 'MoonAirline',
            logo_url = '2'
        )

        Airplane.objects.create(
            id              = 1,
            name            = 'UPG',
            airplane_code   = 35,
            number_of_seats = 100,
            airline_id      = 1
        )

        Airplane.objects.create(
            id              = 2,
            name            = 'HYJ',
            airplane_code   = 35,
            number_of_seats = 100,
            airline_id      = 2
        )

        FlightRoute.objects.create(
            id          = 1,
            code        = 'HN072',
            airplane_id = 1,
            departure   = seoul,
            destination = hawaii
        )

        FlightRoute.objects.create(
            id          = 2,
            code        = 'MO071',
            airplane_id = 2,
            departure   = seoul,
            destination = hawaii
        )

        FlightDetail.objects.create(
            id              = 1,
            departure_time  = '2022-08-11 01:30',
            arrival_time    = '2022-08-11 04:30',
            remaining_seats = 50,
            reserved_seats  = 50,
            price           = 2222222.00,
            flight_route_id = 1 
        )
        
        FlightDetail.objects.create(
            id              = 2,
            departure_time  = '2022-08-11 01:00',
            arrival_time    = '2022-08-11 04:00',
            remaining_seats = 50,
            reserved_seats  = 50,
            price           = 2222222.00,
            flight_route_id = 2 
        )

    def tearDown(self):
        Location.objects.all().delete()
        Airline.objects.all().delete()
        Airplane.objects.all().delete()
        FlightDetail.objects.all().delete()
        FlightRoute.objects.all().delete()

    def test_all_flight_list(self):
        client   = Client()
        response = client.get('/flights?departure_name=Seoul&destination_name=Hawaii&departure_date=11&passenger=1&airline=HoneyAirline&airline=MoonAirline')

        self.assertEqual(response.json(),
            {   
                "departure_list": [
                    {
                        "flight_detail_id"           : 1,
                        "flight_route_code"          : "HN072",
                        "departure_location"         : "Seoul",
                        "departure_location_korean"  : "서울",
                        "departure_airport_code"     : "SEL",
                        "destination_location"       : "Hawaii",
                        "destination_location_korean": "하와이",
                        "destination_airport_code"   : "HNL",
                        "month"                      : 8,
                        "date"                       : 11,
                        "day"                        : 4,
                        "airline"                    : "HoneyAirline",
                        "airline_url"                : "1",
                        "departure_time"             : "01:30",
                        "arrivel_time"               : "04:30",
                        "flight_time"                : "3:00",
                        "price"                      : "2222222.00",
                        "remaining_seats"            : 50,
                        "pssengers"                  : "1"
                    },
                    {
                        "flight_detail_id"           : 2,
                        "flight_route_code"          : "MO071",
                        "departure_location"         : "Seoul",
                        "departure_location_korean"  : "서울",
                        "departure_airport_code"     : "SEL",
                        "destination_location"       : "Hawaii",
                        "destination_location_korean": "하와이",
                        "destination_airport_code"   : "HNL",
                        "month"                      : 8,
                        "date"                       : 11,
                        "day"                        : 4,
                        "airline"                    : "MoonAirline",
                        "airline_url"                : "2",
                        "departure_time"             : "01:00",
                        "arrivel_time"               : "04:00",
                        "flight_time"                : "3:00",
                        "price"                      : "2222222.00",
                        "remaining_seats"            : 50,
                        "pssengers"                  : "1"
                    }
                ],
                "return_list" : []
            }
        )
        self.assertEqual(response.status_code, 200)
