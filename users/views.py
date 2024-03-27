from django.contrib.auth import authenticate, login, logout # authenticate는 username과 password를 돌려주는 함수로 정보가 맞으면 user를 리턴, login은 user를 로그인하는 함수
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import User
from .serializers import PrivateUserSerializer, PublicUserSerializer

class Me(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response(PrivateUserSerializer(user).data)
    
    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data = request.data,
            partial = True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST,
            )

class Users(APIView):
    
    def post(self, request):
        # 이미 serializer에서 중복 검사나, 모델의 유효성 검사를 해준다.
        # 다만, PrivateUserSerializer에서 password 필드를 write_only로 설정했기 때문에 password가 response에 포함되지 않는다.
        # 따라서 password의 varidation을 별도로 해줘야 한다.
        password = request.data.get("password")
        if not password:
            raise ParseError("Password is required.")
        serializer = PrivateUserSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save() # 새로운 user를 생성한다.
            user.set_password(password) # set_password라는 user model의 method를 사용하여 password를 암호화한다.
            user.save() # 암호화된 password를 저장한다.
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST,
            )
            
class PublicUser(APIView):
    
    def get(self, request, username):
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            raise NotFound("User not found.")
        serializer = PublicUserSerializer(user)
        return Response(serializer.data)
    
class ChangePassword(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password") # 기존 비밀번호
        new_password = request.data.get("new_password") # 새로운 비밀번호
        if user.check_password(old_password): # 기존 비밀번호를 확인한다.
            user.set_password(new_password) # 맞으면, 새로운 비밀번호를 암호화한다.
            user.save() # 암호화된 비밀번호를 저장
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class LogIn(APIView):
    # login은 post method로만 동작
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError("Username and Password are required.")
        user = authenticate(
            request, 
            username = username, 
            password = password
        ) # username과 password를 만족하는 user를 찾아 리턴해준다.
        if user: # user가 존재하면
            login(request, user) # user를 로그인한다.
            return Response({"OK" : "welcome"})
        else:
            raise PermissionDenied("Username or Password is wrong.")
        
class LogOut(APIView):
    # logout은 post method로만 동작
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({"OK" : "bye"})