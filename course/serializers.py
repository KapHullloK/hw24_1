from rest_framework import serializers

from course.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lessons_info = LessonSerializer(source='lesson', many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_count_lessons(self, obj):
        return obj.lesson.count()
