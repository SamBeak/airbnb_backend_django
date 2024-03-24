from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from .models import Photo

class PhotoDetail(APIView):
    
    permission_classes = [IsAuthenticated] # 인증 여부를 확인할 수 있는 property 설정, is_authenticated를 확인하지 않아도 된다.
    def get_object(self, pk):
        try:
            return Photo.objects.get(pk = pk)
        except Photo.DoesNotExist:
            raise NotFound("Photo not found.")
    
    def delete(self, request, pk):
        photo = self.get_object(pk)
        if photo.room: # 사진이 방을 가지고 있는지 확인
            if photo.room.owner != request.user: # 방의 주인이 아닌 경우
                raise PermissionDenied("You are not owner.")
        elif photo.experience:
            if photo.experience.host != request.user:
                raise PermissionDenied("You are not owner.")
        photo.delete()
        return Response(status = HTTP_204_NO_CONTENT)