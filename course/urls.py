from django.urls import path
from rest_framework import routers
from course.apps import CourseConfig
from course.views import CourseViewSet, LessonList, LessonRetrieve, LessonCreate, LessonUpdate, LessonDestroy

app_name = CourseConfig.name

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/', LessonList.as_view(), name='lesson-list'),
    path('lessons/<int:pk>', LessonRetrieve.as_view(), name='lesson-retrieve'),
    path('lessons/create/', LessonCreate.as_view(), name='lesson-create'),
    path('lessons/update/<int:pk>', LessonUpdate.as_view(), name='lesson-update'),
    path('lessons/delete/<int:pk>', LessonDestroy.as_view(), name='lesson-destroy'),
] + router.urls
