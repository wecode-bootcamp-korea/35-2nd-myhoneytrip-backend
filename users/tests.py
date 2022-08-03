import json
from django.test   import TestCase, Client
from unittest.mock import patch, MagicMock

from users.models import User
from core.utils   import create_token

class KakaoSigninTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            name     = '닉넴1',
            kakao_id = '1234'
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch('users.views.KakaoAPI')
    def test_success_kakao_signup_and_signin(self, mocked_kakao_api):
        client = Client()
        
        class MockedKakaoResponse:
            def get_kakao_token(self, code):
                return 'mocked_access_token'

            def get_kakao_profile(self, token):
                return {
                    "id":123456789,
                    "kakao_account": { 
                        "profile_needs_agreement": False,
                        "profile": {
                            "nickname": "홍길동",
                            "thumbnail_image_url": "http://yyy.kakao.com/.../img_110x110.jpg",
                            "profile_image_url": "http://yyy.kakao.com/dn/.../img_640x640.jpg",
                            "is_default_image":False
                        },
                        "name_needs_agreement":False, 
                        "name":"홍길동",
                        "email_needs_agreement":False, 
                        "is_email_valid": True,   
                        "is_email_verified": True,
                        "email": "sample@sample.com",
                        "age_range_needs_agreement":False,
                        "age_range":"20~29",
                        "birthday_needs_agreement":False,
                        "birthday":"1130",
                        "gender_needs_agreement":False,
                        "gender":"female"
                    },  
                }

        mocked_kakao_api.return_value = MockedKakaoResponse()

        body     = {'authorize_code':'mocked_auth_code'}
        response = client.post('/users/signin/kakao', json.dumps(body), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
                'message': 'SUCCESS', 
                'token': create_token(2), 
                'name': '홍길동'
                }
            )

    @patch('users.views.KakaoAPI')
    def test_success_kakao_signin(self, mocked_kakao_api):
        client = Client()
        
        class MockedKakaoResponse:
            def get_kakao_token(self, code):
                return 'mocked_access_token'

            def get_kakao_profile(self, token):
                return {
                    "id":1234,
                    "kakao_account": { 
                        "profile_needs_agreement": False,
                        "profile": {
                            "nickname": "닉넴1",
                            "thumbnail_image_url": "http://yyy.kakao.com/.../img_110x110.jpg",
                            "profile_image_url": "http://yyy.kakao.com/dn/.../img_640x640.jpg",
                            "is_default_image":False
                        },
                        "name_needs_agreement":False, 
                        "name":"홍길동",
                        "email_needs_agreement":False, 
                        "is_email_valid": True,   
                        "is_email_verified": True,
                        "email": "sample@sample.com",
                        "age_range_needs_agreement":False,
                        "age_range":"20~29",
                        "birthday_needs_agreement":False,
                        "birthday":"1130",
                        "gender_needs_agreement":False,
                        "gender":"female"
                    },  
                }

        mocked_kakao_api.return_value = MockedKakaoResponse()

        body     = {'authorize_code':'mocked_auth_code'}
        response = client.post('/users/signin/kakao', json.dumps(body), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
                'message': 'SUCCESS', 
                'token': create_token(1), 
                'name': '닉넴1'
                }
            )

    @patch('core.utils.requests')
    def test_fail_invalid_kakao_auth_code(self, mocked_requests):
        client = Client()
        
        class MockedResponseToken:
            def json(self):
                return {
                    'error': 'invalid_grant', 
                    'error_description': 'authorization code not found for code=----', 
                    'error_code': 'KOE320'
                }
            ok = False

        mocked_requests.post = MagicMock(return_value = MockedResponseToken())
        
        body     = {'authorize_code':'mocked_auth_code'}
        response = client.post('/users/signin/kakao', json.dumps(body), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'INVALID_KAKAO_AUTH_CODE'})


    @patch('core.utils.requests')
    def test_fail_invalid_kakao_access_token(self, mocked_requests):
        client = Client()

        class MockedResponseProfile:
            def json(self):
                return {
                    'error': 'invalid_grant', 
                    'error_description': 'authorization code not found for code=----', 
                    'error_code': 'KOE320'
                }
            ok = False

        mocked_requests.get  = MagicMock(return_value = MockedResponseProfile())
        body     = {'authorize_code':'mocked_auth_code'}
        response = client.post('/users/signin/kakao', json.dumps(body), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'INVALID_KAKAO_ACCESS_TOKEN'})

    def test_fail_key_error(self):
        client = Client()

        body = {'auth_code':'mocked_auth_code'}

        response = client.post('/users/signin/kakao', json.dumps(body), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})