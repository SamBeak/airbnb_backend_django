from django.db import models
from common.models import CommonModel

class Review(CommonModel):
    
    """ Review Model Definition """
    
    user = models.ForeignKey(
        "users.User",
        on_delete = models.CASCADE,
        related_name = "reviews",
    )
    room = models.ForeignKey(
        "rooms.Room",
        null = True, # room이 없을 수도 있음
        blank = True, # room이 없을 수도 있음, 댓글이 experience에 달릴 수도 있는 것이니깐.
        on_delete = models.CASCADE,
        related_name = "reviews",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null = True,
        blank = True, # experience가 없을 수도 있음, 댓글이 room에 달릴 수도 있는 것이니깐.
        on_delete = models.CASCADE,
        related_name = "reviews",
    )
    payload = models.TextField() # 댓글 내용
    rating = models.PositiveIntegerField() # 별점
    
    def __str__(self):
        return f"{self.user} / {self.rating}⭐️"