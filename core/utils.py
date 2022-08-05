import jwt

from functools import wraps
from django.http import JsonResponse
from django.conf import settings

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