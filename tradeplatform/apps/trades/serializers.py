from rest_framework import serializers

from apps.registration.serializers import UserSerializer
from apps.trades.models import (Balance, Currency, Inventory, Item, Offer,
                                Price, Trade, WatchList)
from apps.trades.services.views_validators import (
    check_user_balance, check_user_quantity_stocks_for_given_item)


class StockBaseSerializer(serializers.ModelSerializer):
    """Serializer for StockBase base model"""

    code = serializers.CharField(max_length=8)
    name = serializers.CharField(max_length=24)


class CurrencySerializer(StockBaseSerializer):
    """Serializer for Currency model"""

    class Meta:
        model = Currency
        fields = (
            "id",
            "code",
            "name",
        )


class PriceSerializer(serializers.ModelSerializer):
    """Serializer for Price model"""

    currency = CurrencySerializer(read_only=True)
    item = serializers.SlugRelatedField(queryset=Item.objects.all(), slug_field="code")

    class Meta:
        model = Price
        fields = (
            "id",
            "currency",
            "item",
            "price",
            "date",
        )


class PriceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Price instance"""

    class Meta:
        model = Price
        fields = (
            "id",
            "currency",
            "item",
            "price",
            "date",
        )


class ItemSerializer(StockBaseSerializer):
    """Serializer for Item model"""

    price = PriceSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = (
            "id",
            "code",
            "name",
            "price",
            "details",
        )


class BaseUserItemSerializer(serializers.ModelSerializer):
    """Serializer for BaseUserItem base model"""

    user = UserSerializer(read_only=True)
    item = ItemSerializer(read_only=True)


class WatchListSerializer(BaseUserItemSerializer):
    """Serializer for WatchList model"""

    item = ItemSerializer(read_only=True, many=True)

    class Meta:
        model = WatchList
        fields = (
            "id",
            "user",
            "item",
        )


class WatchListCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Watchlist instance"""

    class Meta:
        model = WatchList
        fields = (
            "id",
            "user",
            "item",
        )


class OfferSerializer(BaseUserItemSerializer):
    """Serializer for Offer model"""

    class Meta:
        model = Offer
        fields = (
            "id",
            "status",
            "user",
            "item",
            "entry_quantity",
            "quantity",
            "price",
            "is_active",
        )
        read_only_fields = ("quantity", "is_active")


class OfferCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating offer instance"""

    class Meta:
        model = Offer
        fields = (
            "id",
            "status",
            "item",
            "entry_quantity",
            "quantity",
            "price",
            "is_active",
        )
        read_only_fields = ("quantity", "is_active")

    def validate(self, attrs):
        """Check that new offer instance has correct values in offer's field"""

        if attrs["entry_quantity"] <= 0:
            raise serializers.ValidationError(
                {"entry_quantity": "Entry quantity can't be less than or equal to zero"}
            )
        elif attrs["price"] < 0:
            raise serializers.ValidationError(
                {"price": "Price can't be less than zero"}
            )

        return attrs


class InventorySerializer(BaseUserItemSerializer):
    """Serializer for Inventory model"""

    class Meta:
        model = Inventory
        fields = (
            "id",
            "user",
            "item",
            "quantity",
        )


class BalanceSerializer(serializers.ModelSerializer):
    """Serializer for Balance model"""

    user = UserSerializer(read_only=True)
    currency = CurrencySerializer(read_only=True)

    class Meta:
        model = Balance
        fields = (
            "id",
            "user",
            "currency",
            "quantity",
        )


class TradeSerializer(serializers.ModelSerializer):
    """Serializer for Trade model"""

    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source="item", write_only=True
    )
    seller = serializers.SlugRelatedField(read_only=True, slug_field="username")
    buyer = serializers.SlugRelatedField(read_only=True, slug_field="username")
    buyer_offer = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="offer-detail"
    )
    seller_offer = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="offer-detail"
    )

    class Meta:
        model = Trade
        fields = (
            "id",
            "item",
            "item_id",
            "seller",
            "buyer",
            "quantity",
            "unit_price",
            "description",
            "buyer_offer",
            "seller_offer",
        )
