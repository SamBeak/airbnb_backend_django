from strawberry.permission import BasePermission
from strawberry.types import Info
import typing

class OnlyLoggedIn(BasePermission):
    message = "You must be logged in to do this" # permission이 거부될 때 보여줄 메시지
    # has_permission은 permission이 통과되는지 확인하는 함수로 오버라이드해서 사용
    def has_permission(self, source: typing.Any, info: Info) -> bool: # source는 resolver의 결과값
        return info.context.request.user.is_authenticated # 거짓이 반환되면 permission거부, 참이면 승인