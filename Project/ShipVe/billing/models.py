from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL


# can use this profile to create any profile
# abc@gmail.com -> 100 billing profiles
# login user abc@gmail.com -> 1 billing profile

class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)  # allow guest user to be able to login
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # customer_id in Stripe or Braintree

    def __str__(self):
        return self.email


# customer ID
# def billing_profile_created_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         print("ACTUAL APT REQUEST Send to stripe/braintree")
#         instance.customer_id = newID
#         instance.save()


# automatically create BillingProfile when a user is created
def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)





























