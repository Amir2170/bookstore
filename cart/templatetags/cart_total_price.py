from django import template
from decimal import Decimal

register = template.Library()


@register.simple_tag(takes_context=True)
def cart_total_price(context):
    cart = context['cart']
    sum = 0
    
    for product in cart.values():
        sum += Decimal(product['price'])
    
    return sum    