from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import InventoryTransaction, InventoryItem

@receiver(pre_save, sender=InventoryTransaction)
def validate_transaction(sender, instance, **kwargs):
    """
    Validate transaction before saving (pre_save is better for validation)
    """
    if instance.transaction_type == 'OUT':
        if instance.quantity > instance.item.quantity:
            raise ValidationError(
                f"Cannot remove {instance.quantity} items. "
                f"Only {instance.item.quantity} available in stock."
            )

@receiver(post_save, sender=InventoryTransaction)
def update_inventory_quantity(sender, instance, created, **kwargs):
    """
    Update inventory quantities after successful transaction save.
    Uses atomic transactions for data consistency.
    """
    if created:
        item = instance.item
        with transaction.atomic():
            if instance.transaction_type == 'IN':
                item.quantity += instance.quantity
            elif instance.transaction_type == 'OUT':
                item.quantity -= instance.quantity
            item.save(update_fields=['quantity'])

