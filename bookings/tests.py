import json

import jwt

from django.test import Client, TransactionTestCase

from my_settings import ALGORITHM, SECRET_KEY

from .models import *
from flights.models import *
from users.models import *





class BookingTest(TransactionTestCase):
    def setUp(self):
        User.objects.create(
            id = 1,
            name = 'eumpago',
            kakao_id = '654',
            email = 'eumpago@gmail.com'
        )
        BookingStatus.objects.create(
            id=1
        )
        TicketStatus.objects.create(
            id=1,
        )
        Location.objects.create(
            id=1,
            name='위코드',
            airport_code = '정민힘듬',
            airport_name = '위코드'
        )
        Airline.objects.create(
            id=1,
            name = '위코드공항',
            logo_url = 'dfnjsadfl;kdsjf;lkj;lqnwerjksncv'
        )
        Airplane.objects.create(
            id =1,
            name = '위코드공항',
            airplane_code = 'HEE',
            number_of_seats = 1,
            airline_id = 1
        )
        FlightRoute.objects.create(
            id=1,
            code = 'HS15',
            departure_id = 1,
            destination_id = 1,
            airplane_id = 1
        )
        FlightDetail.objects.create(
            id=1500,
            departure_time = '2012-06-07',
            arrival_time = '2013-06-07',
            flight_route_id = 1,
            remaining_seats = 150,
            reserved_seats = 1,
            price = 150000.00
        )
        FlightDetail.objects.create(
            id=567,
            departure_time = '2022-05-17',
            arrival_time = '2023-06-07',
            flight_route_id = 1,
            remaining_seats = 150,
            reserved_seats = 1,
            price = 150000.00
        )

    def tearDown(self):
        Ticket.objects.all().delete()
        Passenger.objects.all().delete()
        Booking.objects.all().delete()
        User.objects.all().delete()
        BookingStatus.objects.all().delete()
        TicketStatus.objects.all().delete()
        Location.objects.all().delete()
        Airline.objects.all().delete()
        Airplane.objects.all().delete()
        FlightDetail.objects.all().delete()
        FlightRoute.objects.all().delete()

    def test_success_create_booking_data(self):
        payload = {'id' : User.objects.get(id=1).id}
        token   = jwt.encode(payload, SECRET_KEY, ALGORITHM)
        client  = Client()
        header  = {'HTTP_Authorization' : token}

        body = {"booker_name": "황유정",
                "booker_email": "kinguj@gmail.com",
                "booker_mobile_number": "01022886474",
                "flight_detail_id" : [1500, 567],
                "passengers": 
              [{"first_name": "SANGHYUN",
                "last_name": "AHN", 
                "gender": "male", 
                "birthday": "1992-09-15"},
               {"first_name": "JUNGMIN",
                "last_name": "EUM",
                "gender": "female",
                "birthday": "1991-05-17"}]}

        response = client.post('/bookings',json.dumps(body), content_type='application/json', **header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'message' : 'SUCCESS'})

    def test_keyerror_fail_create_booking_data(self):
        payload = {'id' : User.objects.get(id=1).id}
        token   = jwt.encode(payload, SECRET_KEY, ALGORITHM)
        client  = Client()
        header  = {'HTTP_Authorization' : token}

        body = {"booker": "황유정",
                "booker_email": "kinguj@gmail.com",
                "booker_mobile_number": "01022886474",
                "flight_detail_id" : [1500, 567],
                "passengers": 
              [{"first_name": "SANGHYUN",
                "last_name": "AHN", 
                "gender": "male", 
                "birthday": "1992-09-15"},
               {"first_name": "JUNGMIN",
                "last_name": "EUM",
                "gender": "female",
                "birthday": "1991-05-17"}]}

        response = client.post('/bookings',json.dumps(body), content_type='application/json', **header)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message' : 'KEY_ERROR'})

    def test_flight_detail_keyerror_fail_create_booking_data(self):
        payload = {'id' : User.objects.get(id=1).id}
        token   = jwt.encode(payload, SECRET_KEY, ALGORITHM)
        client  = Client()
        header  = {'HTTP_Authorization' : token}

        body = {"booker_name": "황유정",
                "booker_email": "kinguj@gmail.com",
                "booker_mobile_number": "01022886474",
                "flight_detail_id" : [300000, 567],
                "passengers": 
              [{"first_name": "SANGHYUN",
                "last_name": "AHN", 
                "gender": "male", 
                "birthday": "1992-09-15"},
               {"first_name": "JUNGMIN",
                "last_name": "EUM",
                "gender": "female",
                "birthday": "1991-05-17"}]}

        response = client.post('/bookings',json.dumps(body), content_type='application/json', **header)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),{'message' : 'FLIGHT_DETAIL KEY_ERROR'})