from django.shortcuts import render
from django.views.generic import ListView
from . import models
from . import services
from . import helpers
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    """
        renders request to 'templates/index.html'
    """
    return render(request, 'index.html')


def login(request):
    """
        renders request to 'templates/login.html'
    """
    return render(request, 'login.html')

    
class ProductsList(ListView):
    """
        generic listview showing models.Product
        (renders request to 'templates/ecommerce/product_list.html')
    """
    model = models.Product


class ProductCategoriesList(ListView):
    """
        generic listview showing models.ProductCategory
        (renders request to 'templates/ecommerce/productcategory_list.html')
    """
    model = models.ProductCategory


def product_category(request, product_category_pk):
    """
        renders request to 'templates/ecommerce/product_category.html'
        with 'category' and 'products' pulled from the db
    """
    return render(request, 'ecommerce/product_category.html', {
        'category': models.ProductCategory.objects.get(pk=product_category_pk),
        'products': models.Product.objects.filter(category=product_category_pk)
    })


@login_required
def cart(request):
    """
        renders request to 'ecommerce/cart.html'
        with 'cart_items' provided by helpers.Cart

        requires user to be logged in
    """
    user_id = request.user.pk
    return render(request, 'ecommerce/cart.html', {
        'cart_items': helpers.Cart.of(user_id).items
    })


@login_required
def cart_remove_item(request, cart_item_pk):
    """
        passes request to cart(request) view

        tries to remove cart item

        requires user to be logged in
    """
    user_id = request.user.pk
    try:
        helpers.Cart.of(user_id).remove_one(cart_item_pk)
    except models.CartItem.DoesNotExist:
        messages.error(request, 'Cannot remove non existing item from cart')
    return cart(request)


@login_required
def cart_add_product(request, product_pk):
    """
        passes request to ProductsList.as_view() view

        tries to add product to user cart

        requires user to be logged in
    """

    user_id = request.user.pk

    try:
        helpers.Cart.of(user_id).add_one(product_pk)
    except models.Product.DoesNotExist:
        messages.error(request, 'Cannot add non existing product to cart')

    return ProductsList.as_view()(request)
