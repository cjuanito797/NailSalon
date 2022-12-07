from django.shortcuts import render, redirect, get_object_or_404
from Appointments.models import Service
from .cart import Cart
from .forms import CartAddServiceForm


# Create your views here.

def cart_add(request, service_id):
    cart = Cart (request)
    service = get_object_or_404 (Service, id=service_id)
    cart.add (
        service=service,
        quantity=1
    )

    return redirect ('appointments:service_list')  # simply redirect to the page displaying our services.

def cart_update_Quanity(request, service_id):
    if request.method == "POST":
        form = CartAddServiceForm(request.POST)
        if form.is_valid():

            cart = Cart(request)
            service = get_object_or_404(Service, id=service_id)

            # first remove from the cart.
            cart.remove(service)

            # print the service id and the new quantity

            cart.add (
                service=service,
                quantity=int(request.POST["quantity"])
            )
        return redirect('cart:cart_detail')
    else:
        return redirect('cart:cart_detail')


def cart_remove(request, service_id):
    cart = Cart (request)
    service = get_object_or_404 (Service, id=service_id)
    cart.remove (service)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart (request)
    for item in cart:
        item['update_quantity_form'] = CartAddServiceForm (
            initial={
                'quantity': item['quantity'],
                'update': True
            }
        )

    if request.user.is_staff:
        manager = True
        customer = False
    else:
        customer = True
        manager = False
    
    return render (request, 'cart/detail.html', {'cart': cart, 'manager': manager, 'customer': customer})
