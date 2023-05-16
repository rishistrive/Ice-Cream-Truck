from rest_framework import serializers
from food_app.models import FoodItem
from rest_framework import serializers
from food_app.models import FoodItemInventory


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['id', 'truck', 'name', 'price', 'flavors']



class FoodItemInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItemInventory
        fields = '__all__'
