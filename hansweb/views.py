from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Order
from .forms import OrderForm


def home(request):
    return render(request, 'hansweb/home.html', {})


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
    return render(request, 'hansweb/order_details.html', {'order': order})


def order_add(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.client = request.user
            post.created_date = timezone.now()
            post.save()
            return redirect('hansweb/order_details', pk=post.pk)
    else:
        form = OrderForm()
    return render(request, 'hansweb/order_new.html', {'form': form})
