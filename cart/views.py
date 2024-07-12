from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from .models import CartItem
from .serializers import CartItemSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import CartItem
from .serializers import CartItemSerializer
from rest_framework.decorators import action
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    @action(detail=False, methods=['get'], url_path='total')
    def cart_total(self, request):
        user = request.user  # Assuming the user is authenticated
        cart_items = CartItem.objects.filter(user=user)

        total_amount = sum(item.quantity * item.product.price for item in cart_items)

        return Response({"total": total_amount}, status=status.HTTP_200_OK)
