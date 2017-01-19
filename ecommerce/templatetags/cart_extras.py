from django import template
from ecommerce.helpers import Cart

register = template.Library()

@register.filter
def cart_price(user_id):
    try:    return str(Cart.of(user_id).price) + '$'
    except: return ''

@register.filter
def cart_items(user_id):
    try:    return str(Cart.of(user_id).items_count)
    except: return ''
