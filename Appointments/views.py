from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, Category
from cart.forms import CartAddServiceForm


def service_list(request, category_slug=None):
    # function that will be used to display oll of our services.
    category = None
    categories = Category.objects.all ( )
    services = Service.objects.all ( )
    if category_slug:
        category = get_object_or_404 (Category, slug=category_slug)
        services = services.filter (category=category)

    return render (request,
                   'shop/service_list.html',
                   {
                       'category': category,
                       'categories': categories,
                       'services': services

                   })


def service_detail(request, id, slug):
    # function used to display the details of a particular service.
    service = get_object_or_404 (Service,
                                 id=id,
                                 slug=slug,
                                 )
    cart_service_form = CartAddServiceForm ( )

    return render (request,
                   'shop/service_detail.html',
                   {
                       'service': service,
                       'cart_service_form': cart_service_form
                   })
