from rest_framework import serializers

from .models import Feature


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ["id", "title", "description", "votes", "created_at", "updated_at"]
        read_only_fields = ["id", "votes", "created_at", "updated_at"]

    def validate_title(self, value):
        """Ensure title is unique (case-insensitive)"""
        if Feature.objects.filter(title__iexact=value).exists():
            if self.instance and self.instance.title.lower() != value.lower():
                raise serializers.ValidationError(
                    "A feature with this title already exists."
                )
            elif not self.instance:
                raise serializers.ValidationError(
                    "A feature with this title already exists."
                )
        return value


class FeatureCreateSerializer(FeatureSerializer):
    """Serializer for creating features"""

    class Meta(FeatureSerializer.Meta):
        fields = ["title", "description"]


class FeatureUpdateSerializer(FeatureSerializer):
    """Serializer for updating features"""

    class Meta(FeatureSerializer.Meta):
        fields = ["title", "description"]
