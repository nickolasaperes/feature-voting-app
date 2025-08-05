from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Feature
from .serializers import (
    FeatureCreateSerializer,
    FeatureSerializer,
    FeatureUpdateSerializer,
)


class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == "create":
            return FeatureCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return FeatureUpdateSerializer
        return FeatureSerializer

    def get_queryset(self):
        """Filter features based on query parameters"""
        queryset = Feature.objects.all()
        search = self.request.query_params.get("search", None)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        return queryset

    def create(self, request, *args, **kwargs):
        """Create a new feature"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        feature = serializer.save()

        response_serializer = FeatureSerializer(feature)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update a feature"""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        feature = serializer.save()

        response_serializer = FeatureSerializer(feature)
        return Response(response_serializer.data)

    @action(detail=True, methods=["post"])
    def upvote(self, request, pk=None):
        """Upvote a feature"""
        feature = self.get_object()
        feature.upvote()
        return Response(
            {
                "id": feature.id,
                "votes": feature.votes,
                "message": "Feature upvoted successfully",
            }
        )

    @action(detail=True, methods=["post"])
    def downvote(self, request, pk=None):
        """Downvote a feature"""
        feature = self.get_object()
        feature.downvote()
        return Response(
            {
                "id": feature.id,
                "votes": feature.votes,
                "message": "Feature downvoted successfully",
            }
        )

    @action(detail=False, methods=["get"])
    def top_voted(self, request):
        """Get top voted features"""
        limit = int(request.query_params.get("limit", 10))
        features = Feature.objects.order_by("-votes")[:limit]
        serializer = FeatureSerializer(features, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def recent(self, request):
        """Get recently created features"""
        limit = int(request.query_params.get("limit", 10))
        features = Feature.objects.order_by("-created_at")[:limit]
        serializer = FeatureSerializer(features, many=True)
        return Response(serializer.data)

