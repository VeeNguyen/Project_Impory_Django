from django.http import JsonResponse
from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail

from addresses.forms import AddressForm
from addresses.models import Address

from billing.models import BillingProfile
from orders.models import Order
from products.models import Product
from .models import Cart


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    # Query set [<object>, <object>, <object>].
    # So we serialize it by doing this. JsonResponse understands.
    products = [{
                "id": items.id,
                "url": items.get_absolute_url(),
                "name": items.name,
                "price": items.price,
                }
                for items in cart_obj.products.all()]

    cart_data = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    return JsonResponse(cart_data)


def cart_home(request):  # Create an object
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):  # Update that object
    product_id = request.POST.get("product_id")

    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("cart:home")

        cart_obj, new_obj = Cart.objects.new_or_get(request)

        # Adding and Removing products in cart
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
        else:
            cart_obj.products.add(product_obj)
            added = True
        request.session["cart_items"] = cart_obj.products.count()  # Counting the number of items

        # Handling Ajax response on the browser
        # Asynchronous JavaScript And XML / JSON - Javascript Object Notation
        if request.is_ajax():
            print("Ajax request")
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count(),
            }
            # Return Json with a message: return JsonResponse({"message": "Error 400"}, status=400). Default of status is 200/201. Django Rest Framework is perfect for handling Error stuff
            return JsonResponse(json_data, status=200)
    return redirect("cart:home")


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_address_id = request.session.get("billing_address_id", None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None

    # Creating order object
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address_id = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if shipping_address_id or billing_profile:
            order_obj.save()

    # Check if order is done
    if request.method == "POST":
        "check that order is done"
        # update order_obj to 'done' or 'paid'
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect("cart:success")  # Call it by its name in urls.py

    # New stuff that is shown on website should be added in context
    context = {
        "objects": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
    }
    return render(request, "carts/checkout.html", context)


# Done with checkout process
def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})








