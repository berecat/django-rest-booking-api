from rest_framework import serializers
from django.contrib.auth.models import User

from trades.models import (Currency,
                           Item,
                           Price,
                           WatchList,
                           Offer,
                           Inventory,
                           Balance,
                           Trade,
                           )


class StockBaseSerializer(serializers.ModelSerializer):
    """Serializer for StockBase base model"""
    code = serializers.CharField(max_length=8)
    name = serializers.CharField(max_length=24)


class CurrencySerializer(StockBaseSerializer):
    """Serializer for Currency model"""

    class Meta:
        model = Currency
        fields = (
            'id',
            'code',
            'name',
        )


class PriceSerializer(serializers.ModelSerializer):
    """Serializer for Price model"""

    currency = CurrencySerializer(read_only=True)
    currency_id = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all(), source='currency',
                                                     write_only=True)
    item = serializers.SlugRelatedField(queryset=Item.objects.all(), slug_field='code')

    class Meta:
        model = Price
        fields = (
            'id',
            'currency',
            'currency_id',
            'item',
            'price',
            'date',
        )


class ItemSerializer(StockBaseSerializer):
    """Serializer for Item model"""
    price = PriceSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = (
            'id',
            'code',
            'name',
            'price',
            'details',
        )


class BaseUserItemSerializer(serializers.ModelSerializer):
    """Serializer for BaseUserItem base model"""
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    item = serializers.SlugRelatedField(queryset=Item.objects.all(), slug_field='code')


class WatchListSerializer(serializers.ModelSerializer):
    """Serializer for WatchList model"""
    item = ItemSerializer(many=True, read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), many=True, source='item',
                                                 write_only=True)

    class Meta:
        model = WatchList
        fields = (
            'id',
            'user',
            'item',
            'item_id',
        )


class OfferSerializer(BaseUserItemSerializer):
    """Serializer for Offer model"""

    class Meta:
        model = Offer
        fields = (
            'id',
            'status',
            'user',
            'item',
            'entry_quantity',
            'quantity',
            'price',
            'is_active',
        )


class InventorySerializer(BaseUserItemSerializer):
    """Serializer for Inventory model"""

    class Meta:
        model = Inventory
        fields = (
            'id',
            'user',
            'item',
            'quantity',
        )


class BalanceSerializer(serializers.ModelSerializer):
    """Serializer for Balance model"""
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    currency = serializers.SlugRelatedField(queryset=Currency.objects.all(), slug_field='code')

    class Meta:
        model = Balance
        fields = (
            'id',
            'user',
            'currency',
            'quantity',
        )


class TradeSerializer(serializers.ModelSerializer):
    """Serializer for Trade model"""
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), source='item', write_only=True)
    seller = serializers.SlugRelatedField(read_only=True, slug_field='username')
    buyer = serializers.SlugRelatedField(read_only=True, slug_field='username')
    buyer_offer = serializers.HyperlinkedRelatedField(read_only=True, view_name='offer-detail')
    seller_offer = serializers.HyperlinkedRelatedField(read_only=True, view_name='offer-detail')

    class Meta:
        model = Trade
        fields = (
            'id',
            'item',
            'item_id',
            'seller',
            'buyer',
            'quantity',
            'unit_price',
            'description',
            'buyer_offer',
            'seller_offer',
        )