import math
from django.db import models
from django.db.models import CASCADE
from django.db.models.signals import pre_save, post_save

from billing.models import BillingProfile
from ShipVe.utils import unique_order_id_generator
from carts.models import Cart


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)

# Creating orders


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        if qs.count() == 1:  # If it exists
            obj = qs.first()
        else:  # Create new order
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created = True
        return obj, created


# Generating order ids need to be random + unique
# pk (primary key) / id -> 1346827398493


class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=CASCADE)
    order_id = models.CharField(max_length=120, blank=True)  # AB31DE3
    # shipping_address
    # billing address
    cart = models.ForeignKey(Cart, on_delete=CASCADE)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.order_id

    objects = OrderManager()

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        self.save()
        return new_total


# Generating order ids with random unique strings
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    # If you want to create new id every time. Then just get rid of the 'if' statement
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

    # Deactivate before-login-order. Active after-login-order
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(pre_save_create_order_id, sender=Order)


# Generating order total when order is not created
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


# Generating order total when order is created. Fire when update order
def post_save_order(sender, instance, created, *args, **kwargs):
    print("running")
    if created:
        print("updatingggggggggg")
        instance.update_total()


post_save.connect(post_save_order, sender=Order)
