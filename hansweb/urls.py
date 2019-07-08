from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='hansweb/home.html'), name='home_view'),
    path('account_add/', views.account_add_view, name='account_add_view'),
    path('account/', views.account_view, name='account_view'),
    path('orders_all/', views.orders_all_waiting_available_view, name='orders_all_view'),
    path('orders/', views.orders_view, name='orders_view'),
    path('orders/<int:pk>/', views.order_delete_view, name='order_delete_view'),
    path('order/<int:pk>/', views.order_details_view, name='order_details_view'),
    path('orders/new/', views.OrderFormWizardView.as_view(views.OrderFormWizardView.FORMS), name='order_add_view'),
    path('orders/<int:pk>/', views.order_accept_view, name='order_accept_view'),
    path('orders_accepted/', views.orders_accepted_view, name='orders_accepted_view'),
]