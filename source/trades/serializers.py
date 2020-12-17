from rest_framework import serializers
from django.contrib.auth.models import User

from trades.models import (Currency,
                           Item,
                           Price,
                           WatchList,
                           Offer,
                           Inventory,
                           Trade)


class StockBaseSerializer(serializers.ModelSerializer):
    """Serializer for StockBase base model"""
    code = serializers.CharField(max_length=8)
    name = serializers.CharField(max_length=24)


class CurrencySerializer(StockBaseSerializer):
    """Serializer for Currency model"""

    class Meta:
        model = Currency
        fields = (
            'code',
            'name',
        )


class ItemSerializer(StockBaseSerializer):
    """Serializer for Item model"""
    currency = serializers.SlugRelatedField(queryset=Currency.objects.all(), slug_field='code')

    class Meta:
        model = Item
        fields = (
            'code',
            'name',
            'price',
            'currency',
            'details',
        )


class PriceSerializer(serializers.ModelSerializer):
    """Serializer for Price model"""
    currency = serializers.SlugRelatedField(queryset=Currency.objects.all(), slug_field='code')
    item = serializers.SlugRelatedField(queryset=Item.objects.all(), slug_field='code')

    class Meta:
        model = Price
        fields = (
            'currency',
            'item',
            'price',
            'date',
        )


class BaseUserItemSerializer(serializers.ModelSerializer):
    """Serializer for BaseUserItem base model"""
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    item = serializers.SlugRelatedField(queryset=Item.objects.all(), slug_field='code')


class WatchListSerializer(serializers.ModelSerializer):
    """Serializer for WatchList model"""
    item = serializers.SlugRelatedField(queryset=Item.objects.all(), many=True, slug_field='code')

    class Meta:
        model = WatchList
        fields = (
            'user',
            'item',
        )


class OfferSerializer(BaseUserItemSerializer):
    """Serializer for Offer model"""

    class Meta:
        model = Offer
        fields = (
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
            'user',
            'item',
            'quantity',
        )


class TradeSerializer(serializers.ModelSerializer):
    """Serializer for Trade model"""
    item = serializers.SlugRelatedField(queryset=Item.objects.all(), slug_field='code')
    seller = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    buyer = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    buyer_offer = serializers.HyperlinkedRelatedField(queryset=Offer.objects.all(), view_name='offer-detail')
    seller_offer = serializers.HyperlinkedRelatedField(queryset=Offer.objects.all(), view_name='offer-detail')

    class Meta:
        model = Trade
        fields = (
            'item',
            'seller',
            'buyer',
            'quantity',
            'unit_price',
            'description',
            'buyer_offer',
            'seller_offer',
        )