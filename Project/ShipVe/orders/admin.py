from django.contrib import admin

from .models import Order

# this admin is for registering new category 'Order' to the admin on the website

admin.site.register(Order)
