from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from formtools.wizard.views import SessionWizardView

from .forms import OrderForm, AddressForm
from .geocoding import Geocoder
from .models import Order

from .mail import send_email_about_changed_status

class OrderFormWizardView(SessionWizardView):
    FORMS = [('pickup_address', AddressForm),
             ('delivery_address', AddressForm),
             ('order', OrderForm)]
    TEMPLATES = {'pickup_address': "hansweb/order_new.html",
                 'delivery_address': "hansweb/order_new.html",
                 'order': "hansweb/form_order_details.html"}

    def get_template_names(self):
        return [self.TEMPLATES[self.steps.current]]

    @method_decorator(login_required)   # instead of @login_required
    def dispatch(self, *args, **kwargs):
        return super(OrderFormWizardView, self).dispatch(*args, **kwargs)

    def done(self, form_list, form_dict, **kwargs):
        form_items = list(form_dict.values())
        pickup_address = form_items[0].save()
        delivery_address = form_items[1].save()

        order = form_items[2].save(commit=False)
        order.pickupAddress = pickup_address
        order.deliveryAddress = delivery_address
        order.created_date = timezone.now()
        order.client = self.request.user
        order.save()
        return redirect('orders_view')


def home_view(request):
    orders = Order.objects.filter(status=Order.StatusType.waiting).order_by('-created_date')
    return render(request, 'hansweb/home.html', {'orders': orders[:5]})


@login_required
def orders_view(request):
    user = request.user
    if user.is_authenticated:
        orders = Order.objects.filter(client=user)
        return render(request, 'hansweb/orders.html', {'orders': orders, 'user': user})
    else:
        return render(request, 'hansweb/orders.html', {'orders': None, 'user': user})


@login_required
def order_delete_view(request, pk):
    Order.objects.filter(pk=pk).delete()
    return redirect('orders_view')


@login_required
def order_details_view(request, pk):
    order = Order.objects.get(pk=pk)
    geocoder = Geocoder()
    pickupAddressLngLat = geocoder.getLngLat(order.pickupAddress.get_formatted())
    deliveryAddressLngLat = geocoder.getLngLat(order.deliveryAddress.get_formatted())
    return render(request, 'hansweb/order_details.html', {'order': order, 'pickup': pickupAddressLngLat, 'delivery': deliveryAddressLngLat})


# show all available orders (status='Waiting for deliverer', client is not authorized user)
@login_required
def orders_all_waiting_available_view(request):
    orders = Order.objects.filter(status=Order.StatusType.waiting).exclude(client=request.user)
    return render(request, 'hansweb/orders_all.html', {'orders': orders})


@login_required
def orders_accepted_view(request):
    user = request.user
    orders = Order.objects.filter(deliverer=user, status='In transit')
    return render(request, 'hansweb/orders_accepted.html', {'orders': orders})


@login_required
def order_accept_view(request, pk):
    order = Order.objects.get(pk=pk)
    order.accept(request.user)
    order.save()
    send_email_about_changed_status(order)
    return redirect('orders_accepted_view')

@login_required
def order_close_view(request, pk):
    order = Order.objects.get(pk=pk)
    order.close()
    order.save()
    send_email_about_changed_status(order)
    return redirect('orders_accepted_view')



