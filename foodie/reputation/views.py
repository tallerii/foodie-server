from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from foodie.reputation.models import Review
from foodie.reputation.serializers import ListReviewSerializer, CreateReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateReviewSerializer
        return ListReviewSerializer
