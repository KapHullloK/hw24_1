from django.core.management.base import BaseCommand

from course.models import Course, Lesson
from users.models import User, Payment


class Command(BaseCommand):
    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            email='admin@my.com',
            defaults={
                'password': 'admin',
                'is_superuser': True,
                'is_staff': True,
            }
        )
        if created:
            user.set_password('admin')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Суперпользователь создан: admin@my.com | admin'))

        courses_list = []
        for i in range(2):
            course = Course.objects.create(
                name=f'How {i}',
                description="WOW"
            )
            course.save()
            courses_list.append(course)

        lessons_list = []
        for i in range(2):
            lesson = Lesson.objects.create(
                name=f'What is {i}',
                description="asd",
                course=courses_list[i],
            )
            lesson.save()
            lessons_list.append(lesson)

        for i in range(4):
            if i <= 1:
                payment = Payment.objects.create(
                    user=user,
                    course=courses_list[(i + 1) % 2],
                    amount=100 * (i + 1),
                    payment_method='transfer'
                )
            else:
                payment = Payment.objects.create(
                    user=user,
                    lesson=lessons_list[(i + 1) % 2],
                    amount=100 * (i + 1),
                    payment_method='transfer'
                )
            payment.save()

        self.stdout.write(self.style.SUCCESS('База платежей заполнена'))
