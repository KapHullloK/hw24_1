from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, get_object_or_404, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import Course
from users.models import Payment, User, Subscribe
from users.serializers import PaymentSerializer, SubscribeSerializer
from users.services import create_product, create_price, create_session


class PaymentList(ListCreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('lesson', 'course', 'payment_method')
    ordering_fields = ('created_at',)


class SubscribeToCourse(APIView):
    @swagger_auto_schema(
        operation_description="Создание или удаление подписки пользователя на курс.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id', 'course_id', 'payment_id'],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID пользователя'),
                'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID курса'),
                'payment_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID платежа'),
            }
        ),
        responses={
            200: openapi.Response(
                description="Подписка успешно удалена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING,
                                                  description='Подписка удалена')
                    }
                )
            ),
            201: openapi.Response(
                description="Подписка успешно создана",
                schema=SubscribeSerializer
            ),
            400: openapi.Response(
                description="Ошибка валидации данных",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING,
                                                description="Необходимо указать 'user_id', 'course_id' и 'payment_id'"
                                                            "\n\n"
                                                            "Подписку можно оформить только на курс")
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', None)
        course_id = request.data.get('course_id', None)
        payment_id = request.data.get('payment_id', None)

        if user_id is None or course_id is None or payment_id is None:
            return Response(
                {"error": "Необходимо указать 'user_id', 'course_id' и 'payment_id'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, id=user_id)
        course = get_object_or_404(Course, id=course_id)
        payment = get_object_or_404(Payment, id=payment_id)

        subscribe = Subscribe.objects.filter(user=user, course=course, payment=payment)
        if subscribe.exists():
            subscribe.delete()
            return Response(
                {"message": "Подписка удалена"},
                status=status.HTTP_200_OK
            )
        else:

            if payment.lesson:
                return Response(
                    {"error": "Подписку можно оформить только на курс"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            new_sub = Subscribe.objects.create(user=user, course=course, payment=payment)
            serializer = SubscribeSerializer(new_sub)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentCreate(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save()
        if payment.lesson:
            product = create_product(payment.lesson.name)
        else:
            product = create_product(payment.course.name)
        price = create_price(payment.amount, product)
        session_id, payment_url = create_session(price)
        payment.session_id = session_id
        payment.url = payment_url
        payment.save()
