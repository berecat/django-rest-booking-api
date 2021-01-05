from rest_framework import serializers

from apps.registration.serializers import UserSerializer
from apps.trades.models import (Balance, Currency, Inventory, Item,
                                ItemStatistic, Offer, Price, Trade, WatchList)
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


class ItemStatisticSerializer(serializers.ModelSerializer):
    """Serializer for item's statistic"""

    item = ItemSerializer(read_only=True)

    class Meta:
        model = ItemStatistic
        fields = (
            "id",
            "item",
            "max_price",
            "min_price",
            "avg_price",
            "sell_stock_quantity",
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
        elif attrs["status"] == "PURCHASE" and not check_user_balance(
            user_id=self.context.get("request").user.id,
            price=attrs["price"],
            quantity=attrs["entry_quantity"],
        ):
            raise serializers.ValidationError(
                {
                    "user": "You don't have enough money to buy that many quantity of stocks"
                }
            )
        elif attrs[
            "status"
        ] == "SELL" and not check_user_quantity_stocks_for_given_item(
            user_id=self.context.get("request").user.id,
            item_id=attrs["item"].id,
            quantity=attrs["entry_quantity"],
        ):
            raise serializers.ValidationError(
                {
                    "user": "You don't have enough quantity of stocks of this item to sell"
                }
            )

        return attrs

    def create(self, validated_data):
        """If the user didn't confirm his email address, his will be inactive"""

        if not validated_data["user"].profile.is_valid:
            validated_data["is_active"] = False

        return super(OfferCreateSerializer, self).create(validated_data=validated_data)


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
