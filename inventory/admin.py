from django.contrib import admin
from .models import Category, InventoryItem, InventoryTransaction

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "category", "quantity",
        "unit_price", "created_by", "created_at", "updated_at"
    )
    list_filter = ("category", "created_at", "updated_at")
    search_fields = ("name", "description")
    readonly_fields = ("created_by", "created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        """Automatically set created_by when adding a new item"""
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "item", "transaction_type",
        "quantity", "performed_by", "timestamp"
    )
    list_filter = ("transaction_type", "timestamp")
    search_fields = ("item__name", "notes")
    readonly_fields = ("performed_by", "timestamp")

    def save_model(self, request, obj, form, change):
        """Automatically set performed_by on save"""
        if not obj.performed_by:
            obj.performed_by = request.user
        super().save_model(request, obj, form, change)

