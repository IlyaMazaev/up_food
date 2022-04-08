from rest_framework import serializers

from .models import RecipeModel


class RecipeSerializers(serializers.ModelSerializer):
    class Meta:
        model = RecipeModel
        fields = ['name', 'ingredients', 'instructions', 'tags', 'products', 'time', 'portions']
