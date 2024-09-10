from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order,OrderProduct


@receiver(post_save, sender = Order)
def update_order_products_status(sender, instance, **kwargs):
    """
    Updates the status of all OrderProduct items related to the Order when the Order's status changes.
    """
    order_products = OrderProduct.objects.filter(order = instance)

    for item in order_products:

        if item.order_item_status not in ["Cancelled", 'Returned']:            
            item.order_item_status = instance.status
            item.save()
           


@receiver(post_save, sender=OrderProduct)
def update_order_status_if_all_cancelled(sender, instance, **kwargs):
    """
    Updates the Order status to 'Cancelled' if all OrderProduct items are cancelled.
    """
    
    order = instance.order
    
    # Check if all items in the order are cancelled or returned using all function which runs on a generator expression
    all_items_cancelled = all(item.order_item_status == 'Cancelled' for item in order.items.all())
    
    all_items_returned = all(item.order_item_status == 'Returned' for item in order.items.all())
    
    if all_items_cancelled:
        order.status = 'Cancelled'
        order.save()
    if all_items_returned:
        order.status = 'Returned'
        order.save()
        print(order.status)
    
            

