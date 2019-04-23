import math
from django.db import models
from django.db.models import CASCADE
from django.db.models.signals import pre_save, post_save

from ShipVe.utils import unique_order_id_generator
from carts.models import Cart


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)

# generating order ids need to be random + unique


class Order(models.Model):
    # pk (primary key) / id -> 1346827398493
    order_id = models.CharField(max_length=120, blank=True)  # AB31DE3
    # billing_profile
    # shipping_address
    # billing address
    cart = models.ForeignKey(Cart, on_delete=CASCADE)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        self.save()
        return new_total


# generating order ids with random unique strings
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    # if you want to create new id every time
    # then just get rid of the 'if' statement
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)


# generating order total when order is not created
def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


# generating order total when order is created. fire when update order
def post_save_order(sender, instance, created, *args, **kwargs):
    print("running")
    if created:
        print("updatingggggggggg")
        instance.update_total()


post_save.connect(post_save_order, sender=Order)
