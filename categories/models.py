from django.db import models
from common.models import CommonModel

class Category(CommonModel):
    
    """ Category Model Definition """
    class CategoryKindChoices(models.TextChoices):
        ROOM = "rooms", "Rooms"
        EXPERIENCE = "experiences", "Experiences"
        
    name = models.CharField(
        max_length = 50,
    )
        
    kind = models.CharField( # kind 안에 choices를 넣어줌으로써, kind에는 rooms나 experiences만 들어갈 수 있음
        max_length = 15,
        choices = CategoryKindChoices.choices,
    )

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"