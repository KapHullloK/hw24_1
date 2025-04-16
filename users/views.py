from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import Course
from users.models import Payment, User, Subscribe
from users.serializers import PaymentSerializer, SubscribeSerializer


class PaymentList(ListCreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('lesson', 'course_id', 'payment_id_method')
    ordering_fields = ('created_at',)


class SubscribeToCourse(APIView):

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', None)
        course_id = request.data.get('course_id', None)
        payment_id = request.data.get('payment_id', None)

        if user_id is None or course_id is None or payment_id is None:
            return Response(
                {"error": "Необходимо указать 'user_id', 'course_id' и 'payment_id'"}
            )

        user = get_object_or_404(User, id=user_id)
        course = get_object_or_404(Course, id=course_id)
        payment = get_object_or_404(Payment, id=payment_id)

        subscribe = Subscribe.objects.filter(user=user, course=course, payment=payment)
        if subscribe.exists():
            subscribe.delete()
            return Response(
                {"message": "Подписка удалена"}
            )
        else:

            if payment.lesson:
                return Response(
                    {"error": "Подписку можно оформить только на курс"}
                )

            new_sub = Subscribe.objects.create(user=user, course=course, payment=payment)
            serializer = SubscribeSerializer(new_sub)
            return Response(serializer.data)
