import strawberry
import typing
from . import types
from . import queries
from . import mutations
from common.permissions import OnlyLoggedIn

@strawberry.type
class Query:
    all_rooms: typing.List[types.RoomType] = strawberry.field(
        resolver=queries.get_all_rooms,
        permission_classes=[OnlyLoggedIn], # 정의 된 permission을 사용 
    )
    room : typing.Optional[types.RoomType] = strawberry.field(resolver=queries.get_room,)
    # typing.Optional은 Nullable로, Null 과 None을 허용한다는 의미
    
@strawberry.type
class Mutation:
    add_room : typing.Optional[types.RoomType] = strawberry.mutation(
        resolver=mutations.add_room,
        permission_classes=[OnlyLoggedIn],
    )