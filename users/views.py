from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView

from users.models import Payment
from users.serializers import PaymentSerializer


class PaymentList(ListCreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('lesson', 'course', 'payment_method')
    ordering_fields = ('created_at',)
