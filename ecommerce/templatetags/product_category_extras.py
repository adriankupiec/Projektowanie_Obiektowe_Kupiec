from django import template
from ecommerce.helpers import Cart
from ecommerce.models import ProductCategory
register = template.Library()

@register.assignment_tag
def product_categories():
    try:    return ProductCategory.objects.all()
    except: return []
