import json
from django.http  import JsonResponse
from django.views import View

from django.conf  import settings
from core.utils import KakaoAPI, create_token
from .models    import User

class KakaoSignInView(View):
    def post(self, request):
        try:
            
            kakao_authorize_code = json.loads(request.body)['authorize_code']

            kakao_api = KakaoAPI(
                settings.KAKAO_REST_API_KEY, 
                settings.KAKAO_REDIRECT_URI, 
                settings.KAKAO_CLIENT_SECRET)

            kakao_access_token = kakao_api.get_kakao_token(kakao_authorize_code)
            kakao_profile      = kakao_api.get_kakao_profile(kakao_access_token)

            kakao_id = kakao_profile['id']
            name     = kakao_profile['kakao_account']['profile']['nickname']
            email    = kakao_profile['kakao_account'].get('email')

            if not User.objects.filter(kakao_id=kakao_id).exists():
                User.objects.create(name=name, email=email, kakao_id=kakao_id)

            user = User.objects.get(kakao_id=kakao_id)

            return JsonResponse({'message': 'SUCCESS', 'token': create_token(user.id), 'name': user.name}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except ValueError as e:
            return JsonResponse({'message': str(e)}, status=400)