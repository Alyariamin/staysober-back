from app import models
from django.contrib import admin


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user__first_name', 'user__last_name']
    list_per_page = 10
    list_select_related = ['user']
    # inlines = [AddressAdminInline]
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


