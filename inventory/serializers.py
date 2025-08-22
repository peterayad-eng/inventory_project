from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, InventoryItem, InventoryTransaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class InventoryItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        source="category", 
        write_only=True,
        required=False
    )
    created_by = serializers.StringRelatedField(read_only=True)
    total_value = serializers.SerializerMethodField()

    class Meta:
        model = InventoryItem
        fields = [
            'id', 'name', 'description', 'quantity',
            'unit_price', 'category', 'category_id',
            'created_by', 'created_at', 'updated_at', 
            'total_value'
        ]
        read_only_fields = ['quantity', 'created_by', 'created_at', 'updated_at']

    def get_total_value(self, obj):
        return obj.quantity * obj.unit_price

class InventoryTransactionSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=InventoryItem.objects.all())
    item_name = serializers.CharField(source="item.name", read_only=True)
    performed_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = InventoryTransaction
        fields = [
            'id', 'item', 'item_name',
            'transaction_type', 'quantity',
            'notes', 'performed_by', 'timestamp'
        ]
        read_only_fields = ['performed_by', 'timestamp', 'item_name']

    def validate_quantity(self, value):
        """Ensure positive quantity"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value

    def create(self, validated_data):
        """Automatically set performed_by from request user"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['performed_by'] = request.user
        return super().create(validated_data)

