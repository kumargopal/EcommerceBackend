from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Order
from .serializers import OrderSerializer
from django.core.mail import send_mail
from django.db import transaction

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @swagger_auto_schema(request_body=OrderSerializer)
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Send email notification
        send_mail(
            'Order Confirmation',
            'Your order has been placed successfully.',
            'noreply@example.com',
            [request.user.email],
            fail_silently=False,
        )
        return response
