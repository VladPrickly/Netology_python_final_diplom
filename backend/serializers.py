# Верстальщик
from rest_framework import serializers

from backend.image_specs import AVATAR_THUMBNAIL_SPECS, PRODUCT_THUMBNAIL_SPECS
from backend.media import image_url, thumbnail_urls
from backend.models import User, Category, Shop, ProductInfo, Product, ProductParameter, OrderItem, Order, Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'user', 'phone')
        read_only_fields = ('id',)
        extra_kwargs = {
            'user': {'write_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(read_only=True, many=True)
    avatar_url = serializers.SerializerMethodField()
    avatar_thumbnails = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'company', 'position', 'avatar', 'avatar_url',
            'avatar_thumbnails', 'contacts',
        )
        read_only_fields = ('id',)

    def get_avatar_url(self, obj):
        return image_url(obj.avatar)

    def get_avatar_thumbnails(self, obj):
        return thumbnail_urls(obj.avatar, AVATAR_THUMBNAIL_SPECS)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'state',)
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('name', 'category',)


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value',)


class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_parameters = ProductParameterSerializer(read_only=True, many=True)
    image_url = serializers.SerializerMethodField()
    image_thumbnails = serializers.SerializerMethodField()

    class Meta:
        model = ProductInfo
        fields = (
            'id', 'model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'image', 'image_url',
            'image_thumbnails', 'product_parameters',
        )
        read_only_fields = ('id',)

    def get_image_url(self, obj):
        return image_url(obj.image)

    def get_image_thumbnails(self, obj):
        return thumbnail_urls(obj.image, PRODUCT_THUMBNAIL_SPECS)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product_info', 'quantity', 'order',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'order': {'write_only': True}
        }


class OrderItemCreateSerializer(OrderItemSerializer):
    product_info = ProductInfoSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    ordered_items = OrderItemCreateSerializer(read_only=True, many=True)

    total_sum = serializers.IntegerField()
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'ordered_items', 'state', 'dt', 'total_sum', 'contact',)
        read_only_fields = ('id',)
