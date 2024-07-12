from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product
from .serializers import ProductSerializer, BulkProductUploadSerializer
from .tasks import bulk_upload_task  # Import your Celery task

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'stock', 'created_at']
    ordering = ['created_at']

    @swagger_auto_schema(request_body=BulkProductUploadSerializer)
    @action(detail=False, methods=['post'])
    def bulk_upload(self, request):
        serializer = BulkProductUploadSerializer(data=request.data)
        if serializer.is_valid():
            products = serializer.validated_data['products']
            #bulk_upload_task.delay(products)  # Initiate bulk upload asynchronously
            return Response({"status": "bulk upload initiated"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset
