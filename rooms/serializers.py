from rest_framework import serializers
from .models import Room, Amenity
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "pk",
            "name",
            "description",
        )


class RoomDetailSerializer(serializers.ModelSerializer):
    
    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(
        read_only=True,
    )
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    class Meta:
        model = Room
        fields = "__all__"
    
    def get_rating(self, room):
        return room.rating()
    def get_is_owner(self, room):
        request = self.context.get("request") # ["request"]와 get("request")의 차이는 존재하지 않는 key를 찾을 때 발생하는 에러의 유무인데, get은 에러가 발생하지 않는다. 왜냐하면 get은 None을 반환하기 때문이다.
        if request: # request가 존재하면
            return room.owner == request.user
        return False
    
    
    
class RoomListSerializer(serializers.ModelSerializer):
    
    rating = serializers.SerializerMethodField() # SerializerMethodField는 어떤 메서드를 사용할 것인지 지정하는 필드
    is_owner = serializers.SerializerMethodField()
    
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
        )
    
    def get_rating(self, room):
        return room.rating()
    
    def get_is_owner(self, room):
        request = self.context["request"] # context는 view에서 넘겨주는 데이터, key값이 "request"인 데이터를 가져오는 것
        return room.owner == request.user # 방 주인이 request의 user와 같은지 확인