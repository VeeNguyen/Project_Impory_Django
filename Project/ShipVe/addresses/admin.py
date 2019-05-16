from django.contrib import admin

from .models import Address

# this admin is for registering new category 'Address' to the admin on the website

admin.site.register(Address)

