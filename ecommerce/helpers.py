import ecommerce.services
import ecommerce.models


def user_of_cart(cart_id: int):
    """
        returns user associated with given cart(id)
    """
    return ecommerce.models.Cart.objects.get(id=cart_id).user.id

def cart_of_user(user_id: int):
    """
        returns cart associated with given user(id)
    """
    return ecommerce.models.Cart.objects.get_or_create(user=user_id)[0].id

class Cart:
    """
        helper class that uses service's logic in a nice fashion
    """

    def __init__(self, id: int):
        self.id = id
        self.user_id = user_of_cart(id)

    @classmethod
    def of(cls, user_id: int):
        """
            creates cart helper object based on given user(id)
        """
        return cls(cart_of_user(user_id))

    @property
    def price(self):
        """
            returns total price of items in the cart
        """
        return ecommerce.services.calculate_total_cart_price(self.id)

    @property
    def items_count(self):
        """
            returns items stored in the cart
        """
        return ecommerce.services.number_of_items_in_cart(self.id)

    @property
    def items(self):
        return ecommerce.services.get_cart_items_of(self.user_id)

    def remove_one(self, cart_item_id: int):
        """
            decreaces quantity of given item or removes it completely
        """
        ecommerce.services.decrease_quantity_or_remove_item(self.user_id, cart_item_id)

    def add_one(self, product_id: int):
        """
            inserts one more product to a cart
        """
        ecommerce.services.increase_quantity_or_insert_product(self.user_id, product_id)
