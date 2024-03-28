import strawberry
from strawberry import auto
from . import models

@strawberry.django.type(models.Room) # django extension으로 새로운 type의 Room을 지정
class RoomType:
    # room model에서 보여주고 싶은 field들을 지정
    id: auto
    name: auto # auto는 자동으로 type을 지정해줌
    kind: auto