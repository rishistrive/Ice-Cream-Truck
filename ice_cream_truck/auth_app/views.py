import base64
from django.http import Http404
from rest_framework import status, generics
from rest_framework.response import Response
from auth_app.serializers import UserSerializer, TruckSerializer
from auth_app.models import Truck, User
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'success': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        login(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TruckList(APIView):
    """
    API endpoint to list all trucks or create a new truck.
    """
    def get(self, request, format=None):
        trucks = Truck.objects.all()
        serializer = TruckSerializer(trucks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TruckSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TruckDetail(APIView):
    authentication_classes = (BasicAuthentication,)
    
    """
    API endpoint to retrieve, update, or delete a truck by ID.
    """

    def get_object(self, pk):
        try:
            return Truck.objects.get(pk=pk)
        except Truck.DoesNotExist:
            raise Http404("Truck with id '%s' does not exist." % pk)

    def get(self, request, pk, format=None):
        truck = self.get_object(pk)
        serializer = TruckSerializer(truck)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        if len(auth_header) != 2 or auth_header[0].lower() != 'basic':
            # Invalid header format or missing "Basic" prefix
            return Response('Invalid Authorization header', status=400)

        username, password = base64.b64decode(auth_header[1]).decode('utf-8').split(':')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            # Do something with the authenticated user
            truck = self.get_object(pk)
            if truck.user.id == user.id:
                serializer = TruckSerializer(truck, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'It is your truck please select your truckid'})
        else:
            return Response({'message': 'Authentication Failed'})
        
    def delete(self, request, pk, format=None):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        if len(auth_header) != 2 or auth_header[0].lower() != 'basic':
            # Invalid header format or missing "Basic" prefix
            return Response('Invalid Authorization header', status=400)

        username, password = base64.b64decode(auth_header[1]).decode('utf-8').split(':')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            truck = self.get_object(pk)
            if truck.user.id == user.id:
                truck.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'It is your truck please select your truckid'})
        return Response({'message': 'Authentication Failed'})


