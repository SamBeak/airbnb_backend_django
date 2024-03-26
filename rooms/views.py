from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied, ParseError
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated, IsAuthentiacatedOrReadOnly
from django.db import transaction
from .models import Room, Amenity
from categories.models import Category
from . import serializers
from medias.serializers import PhotoSerializer
from reviews.serializers import ReviewSerializer
from django.conf import settings

class Rooms(APIView):
    
    permission_classes = [IsAuthentiacatedOrReadOnly]
    
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = serializers.RoomListSerializer(
            all_rooms, 
            many=True,
            context = {"request": request},
        )
        return Response( serializer.data )
    
    def post(self, request):
        serializer = serializers.RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            # 카테고리 필드 존재 확인
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk = category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCE:
                    raise ParseError("Category cannot be Experience.")
            except Category.DoesNotExist:
                raise NotFound("Category not Found.")
            # 어메니티 필드 존재 확인
            try:
                with transaction.atomic(): # 전부 수행해서 에러 없을 때만 commit
                    room = serializer.save(
                        owner = request.user,
                        category = category,
                    )
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk = amenity_pk)
                        room.amenities.add(amenity)
                        
                    serializer = serializers.RoomDetailSerializer( # 저장된 room을 다시 serializer에 넣어서 반환
                        room,
                        context = {"request": request},
                    )
                    return Response( serializer.data)
            except Exception as e:
                raise ParseError("Amenity not Found.")
        else:
            return Response(
                serializer.errors,
                status = HTTP_400_BAD_REQUEST,
            )
            
class RoomDetail(APIView):
    
    permission_classes = [IsAuthentiacatedOrReadOnly]
    
    def get_room(self, pk):
        try:
            room = Room.objects.get(pk = pk)
        except Room.DoesNotExist:
            raise NotFound("Room not Found.")
        return room
    
    def get(self, request, pk):
        room = self.get_room(pk)
        serializer = serializers.RoomDetailSerializer(
            room,
            context = {"request": request},
        )
        return Response( serializer.data )
    
    def put(self, request, pk):
        room = self.get_room(pk)
        if room.owner != request.user:
            raise PermissionDenied("You are not owner.")
        serializer = serializers.RoomDetailSerializer(
            room,
            data = request.data,
            partial = True,
        )
        if serializer.is_valid(): # 먼저 room에 대한 유효성 검사 후, foreign key에 대한 유효성 검사하여 save 전에 작업 수행하도록.
            if "category" in request.data:
                category_pk = request.data.get("category")
                try:
                    category = Category.objects.get(pk = category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCE:
                        raise ParseError("Category cannot be Experience.")
                    room.category = category # 유효성 검사를 통과했으면 room의 category를 변경, 결국 save 때 반영되는 것을 이용하는 원리.
                except Category.DoesNotExist:
                    raise NotFound("Category not Found.")
                
            if "amenities" in request.data:
                amenities = request.data.get("amenities")
                try:
                    room.amenities.clear() # 기존 amenities를 모두 지우고 시작
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk = amenity_pk)
                        room.amenities.add(amenity)
                except Amenity.DoesNotExist:
                    raise NotFound("Amenity not Found.")
            
            updated_room = serializer.save() # 최종 반영
            return Response( serializers.RoomDetailSerializer(updated_room).data )
        else:
            return Response(
                serializer.errors,
                status = HTTP_400_BAD_REQUEST,
            )
    
    def delete(self, request, pk):
        room = self.get_room(pk)
        if room.owner != request.user:
            raise PermissionDenied("You are not owner.")
        room.delete()
        return Response(status = HTTP_204_NO_CONTENT)
    
class RoomReviews(APIView):
    
    permission_classes = [IsAuthentiacatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk = pk)
        except Room.DoesNotExist:
            raise NotFound("Room not Found.")
        
    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1) # query_params의 page를 가져오고 없으면 1 할당
            page = int(page) # int형 변환
        except ValueError: # int형 변환 오류
            page = 1 # 강제 1 할당
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size # 0부터 시작
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end], # 해당 room의 모든 review를 가져와서 page에 맞게 자르기
            many = True,
        )
        return Response( serializer.data )
    
    def post(self, request, pk):
        serializer = ReviewSerializer(data = request.data)
        if serializer.is_valid():
            review = serializer.save(
                user = request.user,
                room = self.get_object(pk),
            )
            serializer = ReviewSerializer(review)
            return Response( serializer.data )
    
class RoomPhotos(APIView):
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk = pk)
        except Room.DoesNotExist:
            raise NotFound("Room not Found.")
    
    def post(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:
            raise PermissionDenied("You are not owner.")
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(
                room = room,
            )
            serializer = PhotoSerializer(photo)
            return Response( serializer.data )
        else:
            return Response(
                serializer.errors,
                status = HTTP_400_BAD_REQUEST,
            )