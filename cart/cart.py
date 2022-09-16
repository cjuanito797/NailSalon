from decimal import Decimal
from django.conf import settings
from django.contrib.auth import authenticate, login, user_logged_in
from Appointments.models import Service
from cart.models import account_data


class Cart (object):

    def __init__(self, request):
        """
               Initialize the cart.
               """

        self.session = request.session
        cart = self.session.get (settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the services that we currently have in our cart.


        """
        service_ids = self.cart.keys ( )

        # get the service id's and add them to the cart.
        services = Service.objects.filter (id__in=service_ids)

        cart = self.cart.copy ( )
        for service in services:
            cart[str(service.id)]['service'] = service

        for item in cart.values ( ):
            item['price'] = Decimal (item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all of the items in the cart

        """

        return sum(item['quantity'] for item in self.cart.values())


    def add(self, service, quantity=1, update_quantity=False):
        """
        We either add a service to the cart or we update its quantity, if it's ID is in the cart.
        :param service:
        :param quantity:
        :param update_quantity:
        :return: an updated cart.
        """
        service_id = str (service.id)
        if service_id not in self.cart:
            self.cart[service_id] = {'quantity': 0,
                                     'price': str (service.price)}
        if update_quantity:
            self.cart[service_id]['quantity'] = quantity
        else:
            self.cart[service_id]['quantity'] += quantity
        self.save ( )

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, service):
        """
        Remove a product from the cart.
        """
        service_id = str (service.id)
        if service_id in self.cart:
            del self.cart[service_id]
            self.save ( )

    def get_total_price(self):
        return sum (Decimal (item['price']) * item['quantity'] for item in self.cart.values ( ))

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save ( )
