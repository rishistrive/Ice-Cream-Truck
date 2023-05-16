
from django.urls import path
from .views import RegisterView, LoginView, TruckDetail, TruckList


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('trucks/', TruckList.as_view(), name='truck-list'),
    path('trucks/<int:pk>/', TruckDetail.as_view(), name='truck-detail'),
]

    
