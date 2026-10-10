from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class FocusSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    duration_minutes = models.IntegerField(
        validators=[
            MinValueValidator(1), MaxValueValidator(240)
            ])
    session_started = models.DateTimeField()

    def __str__(self):
        return f'{self.user.username}-{self.duration_minutes} minutes'
