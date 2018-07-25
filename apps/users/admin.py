from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    fields = ('name', 'birthdate', 'mobile', 'gender')
    list_display = ('name', 'mobile', 'email', 'gender', 'birthdate')
