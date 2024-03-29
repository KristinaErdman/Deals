from django.urls import path

from .views import APIDeals, APITopCustomers

urlpatterns = [
    path('customers/top/', APITopCustomers.as_view(), name='top_customers'),
    path('deals/', APIDeals.as_view(), name='deals'),
]
