from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from course.models import Course
from hw24_1 import settings
from users.models import Subscribe, User


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


@shared_task
def block_inactive_users() -> int:
    month_ago = timezone.now() - timedelta(days=30)

    users = User.objects.filter(is_active=True, is_superuser=False, last_login__lte=month_ago)
    users.update(is_active=False)

    return users.count()
