from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='hansweb/home.html'), name='home'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:pk>/', views.order_delete, name='order_delete'),
    path('order/<int:pk>/', views.order_details, name='order_details'),
]