from django.urls import path

from users.apps import UsersConfig
from users.views import PaymentList

app_name = UsersConfig.name

urlpatterns = [
    path('payments/', PaymentList.as_view(), name='payment-list'),
]
