from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static # static은 미디어 파일을 제공하기 위한 함수
from django.conf import settings # settings.py 파일을 불러옴

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/rooms/', include('rooms.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 개발 단계에서 미디어 파일을 제공하기 위한 설정
