from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied, ParseError
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from django.db import transaction
from .models import Room, Amenity
from categories.models import Category
from . import serializers

class Rooms(APIView):
    
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