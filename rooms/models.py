from django.db import models
from common.models import CommonModel

class Room(CommonModel):
    """ Room Model Definition """
    
    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = "shared_room", "Shared Room" # ()와 없는 것의 차이점은 튜플로 전달하는지 여부
    
    name = models.CharField(
        max_length = 180,
        default = "",
    )
    country = models.CharField(
        max_length = 50,
        default = "한국",
    )
    city = models.CharField(
        max_length = 80,
        default = "서울",
    )
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(
        max_length = 250,
    )
    pet_friendly = models.BooleanField(
        default = True,
    )
    kind = models.CharField(
        max_length = 20,
        choices = RoomKindChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete = models.CASCADE,
        related_name = "rooms",
    )
    amenities = models.ManyToManyField(
        "rooms.Amenity",
        related_name = "rooms",
    )
    category = models.ForeignKey(
        "categories.Category",
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
        related_name = "rooms",
    )
    
    def __str__(room) -> str:
        return room.name
    
    def total_amenities(room):
        return room.amenities.count()
    
    def rating(room):
        count = room.reviews.count() # reviews는 related_name으로 역참조 관계에 있고 이걸 사용하는 것이다.
        if count == 0:
            return 0
        else:
            total_rating = 0
            for review in room.reviews.all().values("rating"): # "rating"이라는 value만 가져온다.
                total_rating += review["rating"] # rating이라는 키를 가진 value를 누적한다.
                return round(total_rating / count, 2) # 평균을 구하고 소수점 둘째 자리까지 반올림한다.

class Amenity(CommonModel):
    """ Amenity Model Definition """
    
    name = models.CharField(
        max_length = 150,
    )
    description = models.CharField(
        max_length = 150,
        null = True,
        blank = True,
    )
    
    def __str__(amenity) -> str:
        return amenity.name
    
    class Meta:
        verbose_name_plural = "Amenities" # admin페이지의 표시 이름 변경