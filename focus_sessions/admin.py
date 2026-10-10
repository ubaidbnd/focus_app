from django.contrib import admin
from .models import FocusSession
# Register your models here.

class FocusSessionAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj = None):
        if obj:
            return ['user']
        return []
admin.site.register(FocusSession, FocusSessionAdmin)
