from django.contrib import admin # type: ignore
from .models import Order
from django.utils.html import format_html # type: ignore


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "colored_status",
        "total_price",
        "payment_intent_id",
       # "refund_id",
        #"dispute_id",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "id",
        "user__email",
        "payment_intent_id",
        "refund_id",
        "dispute_id",
    )

    readonly_fields = (
        "payment_intent_id",
        "refund_id",
        "dispute_id",
        "created_at",
        "paid_at",
    )

    ordering = ("-created_at",)

    fieldsets = (
        (
            "Order Info",
            {
                "fields": (
                    "user",
                    "status",
                    "total_price",
                )
            },
        ),
        (
            "Payment",
            {
                "fields": (
                    "payment_intent_id",
                    "refund_id",
                    "paid_at",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": ("created_at",),
            },
        ),
    )

    # ---------- Actions ----------
    actions = ["mark_refunded", "mark_disputed"]

    @admin.action(description="Mark selected orders as refunded (manual)")
    def mark_refunded(self, request, queryset):
        queryset.update(status=Order.STATUS_REFUNDED)

    @admin.action(description="Mark selected orders as disputed")
    def mark_disputed(self, request, queryset):
        queryset.update(status=Order.STATUS_DISPUTED)

    # ---------- Visual Status ----------
    @admin.display(description="Status")
    def colored_status(self, obj):
        colors = {
            Order.STATUS_PENDING: "orange",
            Order.STATUS_PAID: "green",
            Order.STATUS_REFUNDED: "blue",
            Order.STATUS_DISPUTED: "red",
            Order.STATUS_CANCELLED: "gray",
        }
        return format_html(
            '<strong style="color:{};">{}</strong>',
            colors.get(obj.status, "black"),
            obj.status.upper(),
        )

    # ---------- Permissions ----------
    def has_delete_permission(self, request, obj=None):
        return False

