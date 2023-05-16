from auth_app.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Truck, FoodItem, FoodItemInventory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import FoodItemInventory
from .serializers import FoodItemInventorySerializer

class BuyFoodItemTestCase1(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="truck_user", email="truckuser@gmail.com", password="set_password", is_truck_owner=True)
        self.truck = Truck.objects.create(user=self.user)
        self.fooditem = FoodItem.objects.create(truck=self.truck, name="abc", price=30, flavors="vanilla")
        self.fooditeminventory = FoodItemInventory.objects.create(food_item=self.fooditem, type="Add", amount_count=5, truck_owner=self.user)

    def test_buy_food_item(self):
        # Test case for successful purchase
        data = {
            'food_item': self.fooditem.id,
            'truck_owner': self.user.id,
            "amount_count":1,
            # Add other required fields for FoodItemInventorySerializer
        }

        response = self.client.post('/food/buy-food-items/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Enjoy')

class BuyFoodItemTestCase2(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="truck_user", email="truckuser@gmail.com", password="set_password", is_truck_owner=True)
        self.truck = Truck.objects.create(user=self.user)
        self.fooditem = FoodItem.objects.create(truck=self.truck, name="abc", price=30, flavors="vanilla")
        self.deducted_inventory = FoodItemInventory.objects.create(food_item=self.fooditem, type="Deduct", amount_count=5, truck_owner=self.user)
        self.add_inventory = FoodItemInventory.objects.create(food_item=self.fooditem, type="Add", amount_count=3, truck_owner=self.user)

    def test_buy_food_item(self):
        # Test case for successful purchase
        data = {
            'food_item': self.fooditem.id,
            'truck_owner': self.user.id,
            "amount_count":1,
            # Add other required fields for FoodItemInventorySerializer
        }

        response = self.client.post('/food/buy-food-items/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Sorry')
        


class FoodItemInventoryListTestCase(APITestCase):
    def setUp(self):
        # Create some sample FoodItemInventory instances for testing
        self.client = APIClient()
        self.user = User.objects.create_user(username="truck_user", email="truckuser@gmail.com", password="set_password", is_truck_owner=True)
        self.truck = Truck.objects.create(user=self.user)
        self.fooditem = FoodItem.objects.create(truck=self.truck, name="abc", price=30, flavors="vanilla")
        self.fooditeminventory1 = FoodItemInventory.objects.create(food_item=self.fooditem, type="Add", amount_count=5, truck_owner=self.user)
        self.fooditeminventory12 = FoodItemInventory.objects.create(food_item=self.fooditem, type="Deduct", amount_count=3, truck_owner=self.user)
        
        # self.inventory1 = FoodItemInventory.objects.create(
        #     food_item=,
        #     amount_count=5,
        #     truck_owner="Owner 1",
        #     type="Add"
        # )
        # self.inventory2 = FoodItemInventory.objects.create(
        #     food_item="Food 2",
        #     amount_count=10,
        #     truck_owner="Owner 2",
        #     type="Deduct"
        # )

    def test_list_food_item_inventories(self):
        url = reverse("food_item_inventory_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            {
                "id": self.fooditeminventory1.id,
                "food_item": self.fooditem.id,
                "amount_count": 5,
                "truck_owner": self.user.id,
                "type": "Add",
            },
            {
                "id": self.fooditeminventory12.id,
                "food_item": self.fooditem.id,
                "amount_count": 3,
                "truck_owner": self.user.id,
                "type": "Deduct",
            },
        ]

        unnecssary_keys = ["created_at", "updated_at", "uuid"]
        
        response_data= [dict(data) for data in response.data]
        for key in unnecssary_keys:
             for data in response_data:
                data.pop(key, None)
        self.assertEqual(response_data, expected_data)
