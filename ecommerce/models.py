from django.db import models
from django.conf import settings
from . import services
from . import helpers
from allauth.account.signals import user_signed_up
from django.dispatch import receiver


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Product categories'


class Product(models.Model):
    name = models.TextField()
    imageurl = models.URLField(null=True, blank=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    category = models.ForeignKey(ProductCategory)

    def __str__(self):
        return '%s that costs %s$' % (self.name, self.price)


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    @property
    def price(self):
        return helpers.Cart(self.id).price

    @property
    def items_count(self):
        return helpers.Cart(self.id).items_count

    def __str__(self):
        return 'cart with id %s that belongs to %s' % (self.id, str(self.user))


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, null=True, blank=True)
    product = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return '%sx %s' % (self.quantity, self.product)

@receiver(user_signed_up)
def create_card(sender, **kwargs):
    user = kwargs.pop('user')
    Cart.objects.create(user=user)
