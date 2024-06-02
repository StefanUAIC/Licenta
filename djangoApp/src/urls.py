from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from users.views import user_router
from problems.views import problems_router
from code_submission.views import code_submission_router
from classes.views import classes_router

api = NinjaAPI()

api.add_router("/users/", user_router)
api.add_router("/problems/", problems_router)
api.add_router("/code_submission/", code_submission_router)
api.add_router("/classes/", classes_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
