import requests
from django.conf import settings
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Product
from shop.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


class RepositoryUpdate(APIView):
    def get(self, request):
        response = requests.get(f"https://api.github.com/repos/{settings.REPOSITORY_NAME}")
        response.raise_for_status()
        response_content = response.json()
        return Response({
            "last_update": response_content.get("updated_at"),
            "last_push": response_content.get("pushed_at")
        })
