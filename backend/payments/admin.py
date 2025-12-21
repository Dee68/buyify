from django.contrib import admin # type: ignore
from .models import WebhookEvent


@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ("event_id", "event_type", "received_at")
    search_fields = ("event_id", "event_type")
    readonly_fields = ("event_id", "event_type", "payload", "received_at")

    def has_add_permission(self, request):
        return False

