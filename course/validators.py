from rest_framework import serializers


class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value.get('link', False) and 'youtube.com' not in value['link']:
            raise serializers.ValidationError('Разрешён только ресурс youtube')
