from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class UserGoal(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    goal = models.IntegerField(validators=
                               [MinValueValidator(30),
                                MaxValueValidator(720)],)
    
    @property
    def display_goal(self):
        if self.goal<60:
            return f'{self.goal} mins'
        hrs = self.goal/60
        if hrs == 1:
            return f"{int(hrs)} hr"
        return f"{hrs:g} hrs"

    def __str__(self):
            return f'{self.user.username}-{self.display_goal}'
