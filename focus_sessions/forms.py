from django import forms
from .models import FocusSession

class FocusSessionForm(forms.ModelForm):
    duration_minutes = forms.IntegerField(min_value=15, max_value=240)
    class Meta:
        model = FocusSession
        fields = ["duration_minutes"]
