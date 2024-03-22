from django.contrib import admin
from .models import Room, Amenity

@admin.action(description="Set all prices to zero") # action은 admin 페이지에서 사용할 수 있는 기능을 만들어줌
def reset_prices(model_admin, request, rooms):
    for room in rooms.all(): # 모든 방을 가져와서 반복문 돌림
        room.price = 0
        room.save() # 저장

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    
    actions = (reset_prices,) # actions는 admin 페이지에서 사용하는 기능 정의
    
    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities", # 함수명을 적어 함수를 사용할 수도 있다.
        "rating", 
        "owner",
        "created_at",
    )
    
    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
        "updated_at",
    )
    
    search_fields = (
        "name",
        "^price", # ^ 시작하는 값 의미
        "=owner__username", #=는 정확한 값 의미, owner의 username을 검색
    )

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )