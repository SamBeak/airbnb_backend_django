from django.urls import path
from .views import Me, Users, PublicUser, ChangePassword, LogIn, LogOut

urlpatterns = [
    path("", Users.as_view()),
    path("me/", Me.as_view()),
    path("change-password/", ChangePassword.as_view()),
    path("log-in/", LogIn.as_view()),
    path("log-out/", LogOut.as_view()),
    path("@<str:username>/", PublicUser.as_view()), # 위랑 순서가 바뀌면, "me"를 str인 username으로 인식해버린다. 그래서 인스타처럼 @를 붙였다.
]