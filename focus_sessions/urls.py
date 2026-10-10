from django.urls import path
from .views import create_focus_session

urlpatterns = [
    path("create_session/", create_focus_session, name="create_session"),
]
