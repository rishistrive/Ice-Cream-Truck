import base64
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from food_app.models import FoodItem
from food_app.serializers import FoodItemSerializer
from .models import FoodItemInventory
from .serializers import FoodItemInventorySerializer
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth import authenticate
from django.db.models import Sum


class FoodItemList(APIView):
    authentication_classes = (BasicAuthentication,)
    """
    List all food items or create a new one.
    """
    def get(self, request):
        food_items = FoodItem.objects.all()
        serializer = FoodItemSerializer(food_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        if len(auth_header) != 2 or auth_header[0].lower() != 'basic':
            # Invalid header format or missing "Basic" prefix
            return Response('Invalid Authorization header', status=400)

        username, password = base64.b64decode(auth_header[1]).decode('utf-8').split(':')
        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                truck = user.truck_set.filter(id=request.data['truck']) 
            except:
                truck = None
                return Response({'message': 'Truck id is not belongs to you'})
            
            serializer = FoodItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Authentication Failed'})


class FoodItemDetail(APIView):
    authentication_classes = (BasicAuthentication,)
    """
    Retrieve, update or delete a food item.
    """
    def get_object(self, pk):
        return get_object_or_404(FoodItem, pk=pk)

    def get(self, request, pk):
        food_item = self.get_object(pk)
        serializer = FoodItemSerializer(food_item)
        return Response(serializer.data)

    def put(self, request, pk):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        if len(auth_header) != 2 or auth_header[0].lower() != 'basic':
            # Invalid header format or missing "Basic" prefix
            return Response('Invalid Authorization header', status=400)

        username, password = base64.b64decode(auth_header[1]).decode('utf-8').split(':')
        user = authenticate(username=username, password=password)
        if user is not None:
            food_item = self.get_object(pk)
            serializer = FoodItemSerializer(food_item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        if len(auth_header) != 2 or auth_header[0].lower() != 'basic':
            # Invalid header format or missing "Basic" prefix
            return Response('Invalid Authorization header', status=400)

        username, password = base64.b64decode(auth_header[1]).decode('utf-8').split(':')
        user = authenticate(username=username, password=password)
        if user is not None:
            food_item = self.get_object(pk)
            food_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class FoodItemInventoryList(APIView):
    authentication_classes = (BasicAuthentication,)
    """
    List all food item inventories, or create a new inventory.
    """
    def get(self, request, format=None):
        food_item_inventories = FoodItemInventory.objects.all()
        serializer = FoodItemInventorySerializer(food_item_inventories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        if len(auth_header) != 2 or auth_header[0].lower() != 'basic':
            # Invalid header format or missing "Basic" prefix
            return Response('Invalid Authorization header', status=400)

        username, password = base64.b64decode(auth_header[1]).decode('utf-8').split(':')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_truck_owner == True:
            serializer = FoodItemInventorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class BuyFoodItem(APIView):

    def post(self, request, format=None):
        filter_add = FoodItemInventory.objects.filter(food_item = request.data['food_item'],truck_owner = request.data['truck_owner'], type="Add").aggregate(add_count=Sum('amount_count'))
        filter_deduct = FoodItemInventory.objects.filter(food_item = request.data['food_item'],truck_owner = request.data['truck_owner'], type="Deduct").aggregate(deduct_count=Sum('amount_count'))
        add_c = (filter_add['add_count'])
        deduct_c = (filter_deduct['deduct_count'])
        request.data['type'] = "Deduct"
        if add_c == None:
            add_c = 0
        if deduct_c == None: 
            deduct_c =0
        if add_c > deduct_c :
            serializer = FoodItemInventorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Enjoy'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Sorry'}, status=status.HTTP_200_OK)

