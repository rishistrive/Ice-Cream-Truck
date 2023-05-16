from django.db import models
from auth_app.models import BaseModel, Truck, User


class FoodItem(BaseModel):
    """
    This model is representing a food item.

    Attributes:
        truck (ForeignKeyField): The truck associated with the food item.
        name (CharField): The name of the food item.
        price (DecimalField): The price of the food item.
        flavors (CharField): The flavors associated with the food item.
        created_at (DateTimeField): The timestamp when the food item was created.
        updated_at (DateTimeField): The timestamp when the food item was last updated.
        uuid (UUIDField): A unique identifier for the food item.
    """
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    flavors = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.name



class FoodItemInventory(BaseModel):
    """
    This model represents the inventory of a specific food item.
    
    Attributes:
        food_item (ForeignKey): The food item associated with this inventory.
        type (CharField): The type of transaction, can be 'Add' or 'Deduct'.
        amount_count (IntegerField): The amount or count of the food item added or deducted.
    """
    ADD = 'Add'
    DEDUCT = 'Deduct'
    TRANSACTION_TYPES = [
        (ADD, 'Add'),
        (DEDUCT, 'Deduct')
    ]
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    type = models.CharField(max_length=6, choices=TRANSACTION_TYPES, default=ADD)
    amount_count = models.PositiveIntegerField()
    truck_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.type} {self.amount_count} {self.food_item.name}(s)"




