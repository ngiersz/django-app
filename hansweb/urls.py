from django.urls import path

from users.views import registration_view, change_password_view, login_view
from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('account_add/', registration_view, name='registration_view'),
    path('account/', change_password_view, name='account_view'),
    path('login/', login_view, name='login_view'),
    path('orders_all/', views.orders_all_waiting_available_view, name='orders_all_view'),
    path('orders/', views.orders_view, name='orders_view'),
    path('orders/<int:pk>/close/', views.order_close_view, name='order_close_view'),
    path('orders/<int:pk>/accept/', views.order_accept_view, name='order_accept_view'),
    path('orders/<int:pk>/delete/', views.order_delete_view, name='order_delete_view'),
    path('order/<int:pk>/', views.order_details_view, name='order_details_view'),
    path('orders/new/', views.OrderFormWizardView.as_view(views.OrderFormWizardView.FORMS), name='order_add_view'),
    path('orders_accepted/', views.orders_accepted_view, name='orders_accepted_view'),
]