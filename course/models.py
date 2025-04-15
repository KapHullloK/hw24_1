from django.db import models

NULLABLE = {
    "blank": True,
    "null": True,
}


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")
    img = models.ImageField(upload_to="course/", verbose_name="img", **NULLABLE)
    description = models.TextField(verbose_name="description", **NULLABLE)

    def __str__(self):
        return f"{self.name}"


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")
    description = models.TextField(verbose_name="description", **NULLABLE)
    img = models.ImageField(upload_to="lesson/", verbose_name="img", **NULLABLE)
    link = models.URLField(verbose_name="link", **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson',
                               verbose_name="course")

    def __str__(self):
        return f"{self.course.name} - {self.name}"
