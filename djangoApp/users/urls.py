from django.urls import path
from ninja import NinjaAPI
from .views import api as user_api

api = NinjaAPI()

api.add_router('/users/', user_api)

urlpatterns = [
    path('api/', api.urls),
]
