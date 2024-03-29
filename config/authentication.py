import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User

class TrustMeBroAuthentication(BaseAuthentication):
    
    def authenticate(self, request): # Authentication class는 authenticate 메소드를 오버라이드(재정의)해야한다.
        username = request.headers.get("Trust-Me") # Trust-Me 는 임의로 설정한 헤더 데이터
        if not username:
            return None # None을 반환하면 permission이 거부된다.
        try:
            user = User.objects.get(username=username)
            return (user, None) # user가 존재하면 user와 None을 튜플로 반환해야한다. 여기서 반환되는 user가 request.user가 된다.
        except User.DoesNotExist:
            raise AuthenticationFailed(f"No user {username}")
        
class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request): # 토큰 복호화
        token = request.headers.get("Jwt") # 암호화된 토큰을 Jwt라는 임의명의 헤더에 담아 보낸 것을 받는다.
        if not token:
            return None
        decode = jwt.decode(
            token, 
            settings.SECRET_KEY,  # 서명 키
            algorithms=["HS256"] # 알고리즘
        ) # 토큰 복호화, 알고리즘은 []가 추가된다.
        pk = decode.get("pk")
        if not pk:
            raise AuthenticationFailed("Invalid token")
        
        try:
            user = User.objects.get(pk=pk)
            return (user, None) # user가 존재하면 user와 None을 튜플로 반환해야한다. 여기서 반환되는 user가 request.user가 된다.
        except User.DoesNotExist:
            raise AuthenticationFailed("No user")