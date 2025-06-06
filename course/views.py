from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from course.models import Course, Lesson
from course.paginators import CoursePaginator
from course.serializers import CourseSerializer, LessonSerializer
from course.tasks import course_update_noti


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            course_update_noti.delay(instance.id)
        return response


class LessonList(ListCreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CoursePaginator


class LessonRetrieve(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonCreate(CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdate(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroy(DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
