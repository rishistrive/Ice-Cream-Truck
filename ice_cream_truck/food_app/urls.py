from django.urls import path
from food_app.views import FoodItemList, FoodItemDetail, FoodItemInventoryList,BuyFoodItem

urlpatterns = [
    path('fooditems/', FoodItemList.as_view(), name='fooditem_list'),
    path('fooditems/<int:pk>/', FoodItemDetail.as_view(), name='fooditem_detail'),
    path('food-item-inventories/', FoodItemInventoryList.as_view(), name='food_item_inventory_list'),
    path('buy-food-items/', BuyFoodItem.as_view(), name='buy_food_item'),
]

