from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token # 이거는 토큰을 받아오는 뷰이다. 이걸 사용하면, 토큰을 받아오는 뷰를 만들 필요가 없다.
from .views import Me, Users, PublicUser, ChangePassword, LogIn, LogOut, JWTLogIn

urlpatterns = [
    path("", Users.as_view()),
    path("me/", Me.as_view()),
    path("change-password/", ChangePassword.as_view()),
    path("log-in/", LogIn.as_view()), # 쿠키를 사용한 login 뷰
    path("log-out/", LogOut.as_view()),
    path("token-login", obtain_auth_token), # auth token 로그인 뷰이다. 이걸 사용하면, 토큰을 받아오는 뷰를 만들 필요가 없다.
    path("jwt-login", JWTLogIn.as_view()), # jwt token을 사용하여 로그인할 때 사용하는 뷰.
    path("@<str:username>/", PublicUser.as_view()), # 위랑 순서가 바뀌면, "me"를 str인 username으로 인식해버린다. 그래서 인스타처럼 @를 붙였다.
]