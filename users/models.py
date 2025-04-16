from django.contrib.auth.models import AbstractUser
from django.db import models

from course.models import Course, Lesson

NULLABLE = {
    "blank": True,
    "null": True,
}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")

    phone = models.CharField(max_length=35, verbose_name="phone", **NULLABLE)
    city = models.CharField(max_length=35, verbose_name="city", **NULLABLE)
    avatar = models.ImageField(upload_to="avatars/", verbose_name="avatar", **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'


class Payment(models.Model):
    PAYMENT_CHOICES = (
        ('cash', 'наличные'),
        ('transfer', 'перевод'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments',
                             verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments',
                               verbose_name="course", **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='payments',
                               verbose_name='lesson', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name="amount")
    payment_method = models.CharField(max_length=35, choices=PAYMENT_CHOICES,
                                      verbose_name="payment method")

    def __str__(self):
        return f'{self.user.email}: {self.course.name}'
