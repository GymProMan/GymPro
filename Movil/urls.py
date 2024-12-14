from django.urls import path
from .views import LoginAPIView, HomeAPIView, EjerciciosAPIView, DatosAPIView

urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/home/', HomeAPIView.as_view(), name='home'),
    path('api/ejercicios/', EjerciciosAPIView.as_view(), name='ejercicios'),
    path('api/datos/', DatosAPIView.as_view(), name='datos'),
]
