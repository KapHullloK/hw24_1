from rest_framework import serializers

from course.models import Course, Lesson
from course.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='link')]


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.IntegerField(read_only=True)
    is_subscribe = serializers.BooleanField(read_only=True)
    lessons_info = LessonSerializer(source='lesson', many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_count_lessons(self, obj: Course) -> int:
        return obj.lesson.count()

    def get_is_subscribe(self, obj: Course) -> bool:
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.subscribers.filter(user=user).exists()
        return False
