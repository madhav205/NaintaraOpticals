from django import template
register = template.Library()

@register.filter
def get_item(cart_items, product_id):
    order = cart_items.get(product_id)
    return order.id if order else None

@register.filter
def get_order_qty(cart_items, product_id):
    order = cart_items.get(product_id)
    return order.quantity if order else 0