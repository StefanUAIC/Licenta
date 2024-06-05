from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from classes.views import classes_router
from code_submission.views import code_submission_router
from problems.views import problems_router
from users.views import user_router

api = NinjaAPI()

api.add_router("/users/", user_router)
api.add_router("/problems/", problems_router)
api.add_router("/code_submission/", code_submission_router)
api.add_router("/classes/", classes_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
