from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Category, InventoryItem, InventoryTransaction
from .serializers import (
    CategorySerializer,
    InventoryItemSerializer,
    InventoryTransactionSerializer
)

# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing categories.
    Only authenticated users can access.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class InventoryItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing inventory items.
    Auto-assigns created_by to request user.
    """
    queryset = InventoryItem.objects.select_related("category", "created_by")
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_queryset(self):
        # Show low stock items
        low_stock = self.request.query_params.get('low_stock')
        queryset = InventoryItem.objects.filter(created_by=self.request.user)
        
        if low_stock:
            queryset = queryset.filter(quantity__lt=10)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Custom endpoint for low stock items"""
        items = self.get_queryset().filter(quantity__lt=10)
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

class InventoryTransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing inventory transactions (Stock In / Out).
    Auto-assigns performed_by.
    """
    queryset = InventoryTransaction.objects.select_related("item", "performed_by")
    serializer_class = InventoryTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter by item_id via query parameter:
        /api/transactions/?item_id=5
        """
        queryset = super().get_queryset()
        item_id = self.request.query_params.get('item_id')
        if item_id is not None:
            queryset = queryset.filter(item_id=item_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(performed_by=self.request.user)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Custom endpoint: /api/transactions/recent/
        Returns the 10 most recent transactions.
        """
        recent_qs = self.get_queryset()[:10]
        serializer = self.get_serializer(recent_qs, many=True)
        return Response(serializer.data)

