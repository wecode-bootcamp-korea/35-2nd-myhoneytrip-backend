from functools   import wraps
from django.http import JsonResponse
from enum         import Enum

import jwt
import requests

from django.conf  import settings
from users.models import User

def check_access(func):
    @wraps(func)
    def wrapper(self, request):
        try: 
            token   = request.headers.get('Authorization', None)
            payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)

            user         = User.objects.get(id = payload['id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)

        return func(self, request)

    return wrapper

class KakaoAPI:
    def __init__(self, rest_api_key, redirect_uri, client_secret):
        self.rest_api_key  = rest_api_key
        self.redirect_uri  = redirect_uri
        self.client_secret = client_secret

    def get_kakao_token(self, authorize_code):
        KAKAO_TOKEN_URL = 'https://kauth.kakao.com/oauth/token'
        headers         = {'Content-Type' : 'application/x-www-form-urlencoded'}
        data            = {
            'grant_type'   : 'authorization_code',
            'client_id'    : self.rest_api_key,
            'redirect_uri' : self.redirect_uri,
            'code'         : authorize_code,
            'client_secret': self.client_secret
        }

        response = requests.post(KAKAO_TOKEN_URL, headers=headers, data=data)

        if not response.ok:
            raise ValueError('INVALID_KAKAO_AUTH_CODE')

        data         = response.json()
        access_token = data.get('access_token')

        return access_token

    def get_kakao_profile(self, access_token):
        KAKAO_PROFILE_URL = 'https://kapi.kakao.com/v2/user/me'
        KAKAO_SIGNOUT_URL = 'https://kapi.kakao.com/v1/user/unlink'

        profile_headers  = {'Authorization':f'Bearer {access_token}'}
        profile_response = requests.get(KAKAO_PROFILE_URL, headers = profile_headers)

        if not profile_response.ok:
            raise ValueError('INVALID_KAKAO_ACCESS_TOKEN')

        profile = profile_response.json()

        signout_headers = {
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {access_token}'
            }
        signout_response = requests.post(KAKAO_SIGNOUT_URL, headers=signout_headers)

        if not signout_response.ok:
            raise ValueError('FAIL_KAKAO_SIGN_OUT')

        return profile

def create_token(value):
    access_token = jwt.encode({'id':value}, settings.SECRET_KEY, settings.ALGORITHM)
    return access_token

class BookingStatusEnum(Enum): 
    UPCOMING = 1
    LAST     = 2
    CANCELED = 3


class TicketStatusEnum(Enum): 
    CONFIRM  = 1
    CANCELED = 2 
