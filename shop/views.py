from rest_framework import permissions, viewsets
from rest_framework.generics import ListAPIView

from shop.models import Product
from shop.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
