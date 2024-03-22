from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    
    """ CUSTOM USER MODEL DEFINITION """
    
    class GenderChoices(models.TextChoices): # TextChoices는 문자열로 된 선택지를 만들어줌
        MALE = ("male", "Male") # ("저장할 값", "화면에 보여질 값")
        FEMALE = ("female", "Female")
    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")
    class CurrencyChoices(models.TextChoices):
        WON = "won", "Korean Won" # ()는 튜플로 전달하지만, 지금은 하나의 값만 전달함
        USD = "usd", "Dollar"

    first_name = models.CharField(
        max_length = 150,
        editable = False, # editable은 admin 페이지에서 수정 가능 여부를 결정
    )
    last_name = models.CharField(
        max_length = 150,
        editable = False,
    )
    avatar = models.URLField(blank=True) # URLField는 URL을 저장할 수 있는 필드
    name = models.CharField(
        max_length = 150,
        default = "",
    )
    is_host = models.BooleanField(default = False)
    gender = models.CharField(
        max_length = 10,
        choices = GenderChoices.choices,
    )
    language = models.CharField(
        max_length = 10,
        choices = LanguageChoices.choices,
    )
    currency = models.CharField(
        max_length = 5,
        choices = CurrencyChoices.choices,
    )