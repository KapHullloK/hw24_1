from rest_framework.test import APITestCase

from course.models import Course
from users.models import User, Payment


class SubscribeTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.course = Course.objects.create(
            name="About W",
            description="look",
        )
        self.user = User.objects.create(
            email='subscribe@test.com',
            password='123'
        )
        self.payment = Payment.objects.create(
            user=self.user,
            course=self.course,
            amount=10,
            payment_method='transfer'
        )

        self.data = {
            'user_id': self.user.pk,
            'course_id': self.course.pk,
            'payment_id': self.payment.pk
        }

    def test_SubscribeToCourse(self):
        response = self.client.post('/users/subscribe/', self.data)

        self.assertEqual(response.json(), {
            'id': 1,
            'user': self.user.pk,
            'course': self.course.pk,
            'payment': self.payment.pk
        })

        response = self.client.post('/users/subscribe/', self.data)

        self.assertEqual(response.json(), {'message': 'Подписка удалена'})
