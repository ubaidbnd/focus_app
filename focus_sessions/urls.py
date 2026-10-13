from django.urls import path
from .views import create_focus_session, show_focus_history

urlpatterns = [
    path("create_session/", create_focus_session, name="create_session"),
    path("focus_history/", show_focus_history, name="focus_history"),
]
