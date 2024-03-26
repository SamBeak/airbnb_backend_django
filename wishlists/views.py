from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied, ParseError
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Wishlist
from rooms.models import Room
from .serializers import WishlistSerializer

class Wishlists(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
        
    def get(self, request):
        all_wishlists = Wishlist.objects.filter(user = request.user) # request.user와 동일한 유저가 가진 wishlist만 가져온다.
        serializer = WishlistSerializer(
            all_wishlists,
            many = True,
            context = {"request": request} # 현재 WishlistSerializer에서 사용 중인 RoomlistSerializer에서 context를 사용하기 때문에 전달이 필요하다.
        )
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WishlistSerializer(data = request.data)
        if serializer.is_valid():
            wishlist = serializer.save(user = request.user)
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status = HTTP_400_BAD_REQUEST,
            )
            
class WishlistDetail(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk, user): # wishlist는 프라이빗이기 때문에 유저 정보도 필요하다.
        try:
            wishlist = Wishlist.obejects.get(pk = pk, user = user)
            return wishlist
        except Wishlist.DoesNotExist:
            raise NotFound("Wishlist not found.")
    
    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)
    
    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            data = request.data,
            partial = True,
        )
        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status = HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status = HTTP_204_NO_CONTENT)
    
class WishlistToggle(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_list(self, pk, user): # wishlist는 프라이빗이기 때문에 유저 정보도 필요하다.
        try:
            wishlist = Wishlist.obejects.get(pk = pk, user = user)
            return wishlist
        except Wishlist.DoesNotExist:
            raise NotFound("Wishlist not found.")
        
    def get_room(self, pk):
        try:
            return Room.objects.get(pk = pk)
        except Room.DoesNotExist:
            raise NotFound("Room not found.")
    
    def put(self, request, pk, room_pk):
        wishlist = self.get_list(pk, request.user)
        room = self.get_room(room_pk) 
        if wishlist.rooms.filter(pk = room.pk).exists(): # filter는 list를 반환하기 때문에 exists()로 존재 여부만 확인한다.
            wishlist.rooms.remove(room) # 이미 있는 경우 지운다.
        else:
            wishlist.rooms.add(room) # 없는 경우 추가한다.
        return Response(status=HTTP_200_OK)