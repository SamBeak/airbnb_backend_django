from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    model = Category
    fields = (
        "pk",
        "name",
        "kind",
    )