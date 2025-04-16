from django.urls import path

from users.apps import UsersConfig
from users.views import PaymentList, SubscribeToCourse

app_name = UsersConfig.name

urlpatterns = [
    path('payments/', PaymentList.as_view(), name='payment-list'),
    path('subscribe/', SubscribeToCourse.as_view(), name='subscribe-to-course'),
]
