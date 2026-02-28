from rest_framework import serializers
from .models import ShortURL, Click

class ShortURLSerializer(serializers.ModelSerializer):
    """Serializer for ShortURL model."""
    class Meta:
        model = ShortURL
        fields = ['id', 'original_url', 'shortened_url', 'created_at']
        read_only_fields = ['id', 'shortened_url', 'created_at']


class ClickSerializer(serializers.ModelSerializer):
    """Serializer for Click model."""
    class Meta:
        model = Click
        fields = ['id', 'clicked_at']
        read_only_fields = ['id', 'clicked_at']
