from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='hansweb/home.html'), name='home'),
    path('account_add/', views.account_add, name='account_add'),
    path('account/', views.account, name='account'),
    path('orders_all/', views.orders_all_waiting_available, name='orders_all'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:pk>/', views.order_delete, name='order_delete'),
    path('order/<int:pk>/', views.order_details, name='order_details'),
    path('orders/new/', views.order_add, name='order_add'),
    path('orders/<int:pk>', views.order_accept, name='order_accept'),
    path('orders_accepted', views.orders_accepted, name='orders_accepted'),
]