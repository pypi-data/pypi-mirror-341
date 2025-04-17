from django.contrib import admin
from .models import FacebookEventLog

@admin.register(FacebookEventLog)
class FacebookEventLogAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'status_code', 'source_url', 'created_at')
    list_filter = ('event_name', 'status_code')
    search_fields = ('source_url', 'response_text')
    readonly_fields = ('event_name', 'status_code', 'response_text', 'source_url', 'created_at')
