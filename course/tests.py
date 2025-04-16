from rest_framework import status
from rest_framework.test import APITestCase

from course.models import Lesson, Course


class LessonTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.course = Course.objects.create(
            name="About W",
            description="look",
        )
        self.lesson = Lesson.objects.create(
            name="Economy",
            description="easy",
            course=self.course
        )
        self.data = {
            'name': 'Economy',
            'description': 'easy',
            'course': self.course.pk
        }

    def test_LessonList(self):
        response = self.client.get('/lessons/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], [
            {'id': self.lesson.pk,
             'name': 'Economy',
             'description': 'easy',
             'img': None,
             'link': None,
             'course': self.course.pk}
        ])

    def test_LessonRetrieve(self):
        response = self.client.get(f'/lessons/{self.lesson.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'id': self.lesson.pk,
            'name': 'Economy',
            'description': 'easy',
            'img': None,
            'link': None,
            'course': self.course.pk
        })

    def test_LessonCreate(self):
        response = self.client.post('/lessons/create/', self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            'id': response.json()['id'],
            'name': 'Economy',
            'description': 'easy',
            'img': None,
            'link': None,
            'course': self.course.pk
        })

    def test_LessonUpdate(self):
        response = self.client.patch(f'/lessons/update/{self.lesson.id}', {'name': 'Business'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'id': self.lesson.pk,
            'name': 'Business',
            'description': 'easy',
            'img': None,
            'link': None,
            'course': self.course.pk
        })

    def test_LessonDestroy(self):
        response = self.client.delete(f'/lessons/delete/{self.lesson.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
