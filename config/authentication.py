from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from users.models import User

class TrustMeBroAuthentication(BasePermission):
    
    def authenticate(self, request): # Authentication class는 authenticate 메소드를 오버라이드(재정의)해야한다.
        username = request.headers.get("Trust-Me") # Trust-Me 는 임의로 설정한 헤더 데이터
        if not username:
            return None # None을 반환하면 permission이 거부된다.
        try:
            user = User.objects.get(username=username)
            return (user, None) # user가 존재하면 user와 None을 튜플로 반환해야한다. 여기서 반환되는 user가 request.user가 된다.
        except User.DoesNotExist:
            raise AuthenticationFailed(f"No user {username}")