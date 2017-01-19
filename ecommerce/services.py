import ecommerce.models

def calculate_total_cart_price(cart_id):
    # gathers cart items of given cart
    items = ecommerce.models.CartItem.objects.filter(cart=cart_id)
    #sums up the price with sigma(price*quantity) formula
    result = 0
    for item in items:
        result += item.product.price * item.quantity
    return result

def number_of_items_in_cart(cart_id):
    # gathers cart items of given cart
    items = ecommerce.models.CartItem.objects.filter(cart=cart_id)
    #sums up the count of items with sigma(quantity) formula
    result = 0
    for item in items:
        result += item.quantity
    return result

def get_cart_items_of(user_id):
    # find or create cart of user
    cart = ecommerce.models.Cart.objects.get_or_create(user=user_id)[0]
    # return cart items related to the cart
    return ecommerce.models.CartItem.objects.filter(cart=cart.pk)

def decrease_quantity_or_remove_item(user_id, cart_item_pk):
    cart_item = ecommerce.models.CartItem.objects.get(pk=cart_item_pk)

    # user cart doesn't contain this particular item
    if cart_item.cart.user.pk != user_id:
        raise ecommerce.models.CartItem.DoesNotExist

    # if cart contains more than one item of such a kind
    if cart_item.quantity > 1:
        # then decreate it's quantity
        cart_item.quantity -= 1
        cart_item.save()
    else:
        # delete item otherwise
        cart_item.delete()

def increase_quantity_or_insert_product(user_id, product_pk):
    # gets product by given id
    product = ecommerce.models.Product.objects.get(pk=product_pk)
    # gets cart of user
    cart = ecommerce.models.Cart.objects.get_or_create(user=user_id)[0]
    #tries to add item
    try:
        # if such a product was inserted to this particular cart, then increase it's quantity
        cart_item = ecommerce.models.CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except ecommerce.models.CartItem.DoesNotExist:
        # create item otherwise
        ecommerce.models.CartItem.objects.create(cart=cart, product=product, quantity=1)
