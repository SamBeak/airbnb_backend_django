from django.db import models
from common.models import CommonModel

class Wishlist(CommonModel):
    """ Wishlist Model Definition """
    name = models.CharField(
        max_length = 150,
    )
    rooms = models.ManyToManyField(
        "rooms.Room",
        related_name = "wishlists", # related_name은 역접근자 이름을 지정해줌
    )
    experiences = models.ManyToManyField(
        "experiences.Experience",
        related_name="wishlists",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete = models.CASCADE,
        related_name = "wishlists",
    )

    def __str__(self) -> str:
        return self.name
