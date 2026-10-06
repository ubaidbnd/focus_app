from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, UserGoal

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "username"]


def get_duration_choices():
    choices = []

    for minutes in range(30, 721, 30):
        if minutes < 60:
            label = f'{minutes} minutes'
        else:
            hrs = minutes / 60
            label = f'{int(hrs)} hr' if hrs == 1 else f'{hrs:g} hrs'
        choices.append((minutes, label))

    return choices


class UserGoalForm(forms.ModelForm):
    goal = forms.ChoiceField(choices=get_duration_choices())
    
    class Meta:
        model = UserGoal
        fields = ["goal"]








    