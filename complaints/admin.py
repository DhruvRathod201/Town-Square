from django.contrib import admin
from django.utils.html import format_html
from .models import Citizen, Complaint, ComplaintUpdate

@admin.register(Citizen)
class CitizenAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'state', 'created_at']
    list_filter = ['city', 'state', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'city']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'citizen', 'category', 'status', 'location', 'created_at', 'image_preview']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'description', 'location', 'citizen__user__username']
    readonly_fields = ['created_at', 'updated_at', 'resolved_at', 'predicted_category']
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('citizen', 'title', 'description', 'location')
        }),
        ('Classification', {
            'fields': ('category', 'predicted_category', 'image')
        }),
        ('Status', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'resolved_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'
    
    def city(self, obj):
        return obj.citizen.city or 'Unknown'
    city.short_description = 'City'

@admin.register(ComplaintUpdate)
class ComplaintUpdateAdmin(admin.ModelAdmin):
    list_display = ['complaint', 'status', 'updated_by', 'created_at']
    list_filter = ['status', 'created_at', 'updated_by']
    search_fields = ['complaint__title', 'notes', 'updated_by__username']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Update Information', {
            'fields': ('complaint', 'status', 'notes', 'updated_by')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
