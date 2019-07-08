from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Order
from .geocoding import Geocoder
from formtools.wizard.views import SessionWizardView
from .forms import OrderForm, AddressForm


class OrderFormWizardView(SessionWizardView):
    template_name = 'hansweb/order_new.html'
    form_list = [AddressForm, AddressForm, OrderForm]

    def done(self, form_list, form_dict, **kwargs):
        print(form_dict)
        form_data = [form.cleaned_data for form in form_list]
        print(form_data[0])
        print(form_data[1])
        print(form_data[2])

        form_items = list(form_dict.values())
        pickup_address = form_items[0].save()
        delivery_address = form_items[1].save()

        order = form_items[2].save(commit=False)
        order.pickupAddress = pickup_address
        order.deliveryAddress = delivery_address
        order.created_date = timezone.now()
        order.client = User.objects.get_by_natural_key('admin')
        order.save()

        return redirect('orders_view')


def home_view(request):
    return render(request, 'hansweb/home.html', {})


def account_add_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home_view')
    else:
        form = UserCreationForm()
    return render(request, 'hansweb/account_add.html', {'form': form})


@login_required
def account_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated!')
            return redirect('account_view')
        else:
            messages.error(request, "Password change failed!")
    else:
        form = PasswordChangeForm(request.user, request.POST)
    return render(request, 'hansweb/account.html', {'form': form})


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
    orders = Order.objects.filter(deliverer=user)
    return render(request, 'hansweb/orders_accepted.html', {'orders': orders})


@login_required
def order_accept_view(request, pk):
    order = Order.objects.get(pk=pk)
    order.accept(request.user)
    order.save()
    return redirect('orders_accepted_view')



