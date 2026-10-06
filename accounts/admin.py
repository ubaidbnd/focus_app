from django.contrib import admin
from .models import User, UserGoal
# Register your models here.

admin.site.register(User)

class UserGoalAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj = None):
        if obj:
            return ['user']
        return []
admin.site.register(UserGoal, UserGoalAdmin)