from django.urls import path, re_path
from .views import SignUp, set_goal, remove_goal


urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('set_goal/', set_goal, name='set_goal'),
    path('remove_goal/', remove_goal, name='remove_goal'),
]
