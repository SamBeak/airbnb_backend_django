from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Review

class WordFilter(admin.SimpleListFilter): # SimpleListFilter는 필터를 만들어주는 클래스
    
    title = "Filter by word" # 필터의 이름
    
    parameter_name = "word" # 필터의 url parameter 이름
    
    def lookups(self, request, model_admin):
        return [
            ("good", "Good"), # (url parameter, 필터 이름)
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]
    
    def queryset(self, request, reviews): # reviews는 Review의 QuerySet
        word = self.value() # url parameter를 가져옴
        if word: # url parameter가 있으면
            return reviews.filter(payload__contains=word) # payload에 word가 포함된 것만 필터링
        else:
            reviews # url parameter가 없으면 모든 것을 반환

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    
    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )