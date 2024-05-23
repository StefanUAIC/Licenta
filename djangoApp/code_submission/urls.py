from django.urls import path
from src.urls import api

urlpatterns = [
    path('api/', api.urls),
]
