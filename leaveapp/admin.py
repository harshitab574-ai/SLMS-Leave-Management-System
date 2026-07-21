from django.contrib import admin
from .models import Staff, Leave


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'department')
    search_fields = ('name', 'email', 'department')


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff', 'from_date', 'to_date', 'status')
    list_filter = ('status',)
    search_fields = ('staff__name',)