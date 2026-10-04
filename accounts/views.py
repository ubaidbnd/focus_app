from django.shortcuts import render
from .forms import CreateUserForm
from django.views import generic
from .models import User
from django.urls import reverse_lazy

# Create your views here.

class SignUp(generic.CreateView):
    model = User
    form_class = CreateUserForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"