from rest_framework import serializers
from .models import ShortURL, Click

class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ['id', 'original_url', 'shortened_url', 'created_at']


class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = ['id', 'clicked_at']