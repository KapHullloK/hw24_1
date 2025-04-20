from celery import shared_task
from django.core.mail import send_mail

from course.models import Course
from hw24_1 import settings
from users.models import Subscribe


@shared_task
def course_update_noti(course_id) -> None:
    course = Course.objects.get(id=course_id)
    subscribes = Subscribe.objects.filter(course=course)
    recipients = []

    for sub in subscribes:
        recipients.append(sub.user.email)

    if recipients:
        send_mail(
            subject=f"Курс '{course.name}' обновился",
            message=f"Курс '{course.name}' был обновлен. Проверьте новые материалы!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipients,
        )
