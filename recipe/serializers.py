from rest_framework import serializers

from .models import RecipeModel


class RecipeSerializers(serializers.ModelSerializer):
    class Meta:
        model = RecipeModel
        fields = ['name', 'ingredients', 'bonded_ingredients', 'how_to_cook', 'time', 'portions', 'types', 'photo_address']
