from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from classes.views import classes_router
from code_submission.views import code_submission_router
from homeworks.views import homework_router
from issues.views import issues_router
from notifications.views import notifications_router
from posts.views import posts_router
from problems.views import problems_router
from solutions.views import solutions_router
from users.views import user_router

api = NinjaAPI()

api.add_router("/users", user_router)
api.add_router("/problems", problems_router)
api.add_router("/code_submission", code_submission_router)
api.add_router("/classes", classes_router)
api.add_router("/solutions", solutions_router)
api.add_router("/homeworks", homework_router)
api.add_router("/posts", posts_router)
api.add_router("/notifications", notifications_router)
api.add_router("/issues", issues_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
