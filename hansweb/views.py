from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .models import Order
from .forms import OrderForm
from .geocoding import Geocoder


def home(request):
    return render(request, 'hansweb/home.html', {})


def account_add(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'hansweb/account_add.html', {'form': form})


def account(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated!')
            return redirect('account')
        else:
            messages.error(request, "Password change failed!")
    else:
        form = PasswordChangeForm(request.user, request.POST)
    return render(request, 'hansweb/account.html', {'form': form})


def orders(request):
    user = request.user
    if user.is_authenticated:
        orders = Order.objects.filter(client=user)
        return render(request, 'hansweb/orders.html', {'orders': orders, 'user': user})
    else:
        return render(request, 'hansweb/orders.html', {'orders': None, 'user': user})


def order_delete(request, pk):
    Order.objects.filter(pk=pk).delete()
    return orders(request)


def order_details(request, pk):
    order = Order.objects.get(pk=pk)
    geocoder = Geocoder()
    pickupAddressLngLat = geocoder.getLngLat(order.pickupAddress.getAddressWithoutZipCodeAndFlat())
    deliveryAddressLngLat = geocoder.getLngLat(order.deliveryAddress.getAddressWithoutZipCodeAndFlat())
    return render(request, 'hansweb/order_details.html', {'order': order, 'pickup': pickupAddressLngLat, 'delivery': deliveryAddressLngLat})


def order_add(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user
            order.created_date = timezone.now()
            order.save()
            return redirect('order_details', pk=order.pk)
    else:
        form = OrderForm()
        dimensions = Order.DimensionType.labels
    return render(request, 'hansweb/order_new.html', {'form': form, 'dimensions': dimensions})


# show all available orders (status='Waiting for deliverer', client is not authorized user)
def orders_all_waiting_available(request):
    orders = Order.objects.filter(status=Order.StatusType.waiting).exclude(client=request.user)
    return render(request, 'hansweb/orders_all.html', {'orders': orders})


def order_accept(request, pk):
    order = Order.objects.get(pk=pk)
    order.accept(request.user)
    order.save()
    return redirect('home')


def orders_accepted(request):
    user = request.user
    orders = Order.objects.filter(deliverer=user)
    return render(request, 'hansweb/orders_accepted.html', {'orders': orders})
