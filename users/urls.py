from django.urls import path

from .views import KakaoSignInView

urlpatterns = [
    path('/signin/kakao', KakaoSignInView.as_view()),
]