from django_filters import DateTimeFilter, FilterSet, NumberFilter

from apps.trades.models import Balance, Inventory, Offer, Price, Trade


class PriceFilter(FilterSet):
    """Filter class for Price model"""

    from_date = DateTimeFilter(field_name="date", lookup_expr="gte")
    to_date = DateTimeFilter(field_name="date", lookup_expr="lte")
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Price
        fields = (
            "item__code",
            "currency__code",
            "min_price",
            "price",
            "max_price",
            "from_date",
            "date",
            "to_date",
        )


class OfferFilter(FilterSet):
    """Filter class for Offer model"""

    min_entry_quantity = NumberFilter(field_name="entry_quantity", lookup_expr="gte")
    max_entry_quantity = NumberFilter(field_name="entry_quantity", lookup_expr="lte")
    min_quantity = NumberFilter(field_name="quantity", lookup_expr="gte")
    max_quantity = NumberFilter(field_name="quantity", lookup_expr="lte")
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Offer
        fields = (
            "status",
            "user__username",
            "min_entry_quantity",
            "entry_quantity",
            "max_entry_quantity",
            "min_quantity",
            "quantity",
            "max_quantity",
            "min_price",
            "price",
            "max_price",
            "is_active",
        )


class InventoryFilter(FilterSet):
    """Filter class for Inventory model"""

    min_quantity = NumberFilter(field_name="quantity", lookup_expr="gte")
    max_quantity = NumberFilter(field_name="quantity", lookup_expr="lte")

    class Meta:
        model = Inventory
        fields = (
            "user__username",
            "item__code",
            "min_quantity",
            "quantity",
            "max_quantity",
        )


class BalanceFilter(FilterSet):
    """Filter class for Balance model"""

    min_quantity = NumberFilter(field_name="quantity", lookup_expr="gte")
    max_quantity = NumberFilter(field_name="quantity", lookup_expr="lte")

    class Meta:
        model = Balance
        fields = (
            "user__username",
            "currency__code",
            "min_quantity",
            "quantity",
            "max_quantity",
        )


class TradeFilter(FilterSet):
    """Filter class for Trade model"""

    min_unit_price = NumberFilter(field_name="unit_price", lookup_expr="gte")
    max_unit_price = NumberFilter(field_name="unit_price", lookup_expr="lte")
    min_quantity = NumberFilter(field_name="quantity", lookup_expr="gte")
    max_quantity = NumberFilter(field_name="quantity", lookup_expr="lte")

    class Meta:
        model = Trade
        fields = (
            "item__code",
            "seller__username",
            "buyer__username",
            "min_unit_price",
            "unit_price",
            "max_unit_price",
            "min_quantity",
            "quantity",
            "max_quantity",
        )
