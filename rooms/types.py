import strawberry
import typing
from strawberry import auto
from strawberry.types import Info
from django.conf import settings
from . import models
from wishlists import models as wishlist_models
from users.types import UserType
from reviews.types import ReviewType

@strawberry.django.type(models.Room) # django extension으로 새로운 type의 Room을 지정
class RoomType:
    # room model에서 보여주고 싶은 field들을 지정
    id: auto
    name: auto # auto는 자동으로 type을 지정해줌
    kind: auto
    owner: "UserType" # 관계형 relation을 지정하는 방법, type만 지정해주면 관계는 자동으로 설정됨
    
    @strawberry.field
    def reviews(self, page:typing.Optional[int] = 1) -> typing.List["ReviewType"]: # type안에 함수를 만들어 사용하는 방법
        # typing.Optional에 의해 page는 필수가 아닌 선택적인 인자가 됨, default 값은 1
        page_size = settings.PAGE_SIZE
        start = (page-1) * page_size
        end = start + page_size
        return self.reviews.all()[start:end] # pagenation 구현
    
    @strawberry.field
    def is_owner(self, info:Info) -> bool: # info parameter는 request 정보를 담고 있음, Info 타입 지정 필요
        return self.owner == info.context.request.user # 현재 user가 owner인지 확인
    
    @strawberry.field
    def is_liked(self, info:Info) -> bool:
        return wishlist_models.Wishlist.objects.filter(
            user = info.context.request.user,
            room_pk = self.pk
        ).exists() # 현재 user가 해당 room을 좋아하는지 확인