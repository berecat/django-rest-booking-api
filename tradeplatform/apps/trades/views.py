from apps.trades.models import (Balance, Currency, Inventory, Item, Offer,
                                Price, Trade, WatchList)
from apps.trades.serializers import (BalanceSerializer, CurrencySerializer,
                                     InventorySerializer, ItemSerializer,
                                     OfferSerializer, PriceSerializer,
                                     TradeSerializer, WatchListSerializer)
from apps.trades.services.db_interaction import delete_offer_by_id
from apps.trades.services.views_logic import setup_user_attributes
from rest_framework import mixins, viewsets


class CurrencyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet for Currency model"""

    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class ItemViewSet(viewsets.ModelViewSet):
    """ViewSet for Item model"""

    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class PriceViewSet(viewsets.ModelViewSet):
    """ViewSet for Price model"""

    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class WatchListViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet for WatchList model"""

    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer


class OfferViewSet(viewsets.ModelViewSet):
    """ViewSet for Offer model"""

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def perform_create(self, serializer):
        """
        When receive post method, connect offer instance with current user.
        Also will create balance for the user, if it doesn't exist
        """

        user = self.request.user
        setup_user_attributes(user_id=user.id)

        serializer.save(user=user)

    def perform_destroy(self, instance):
        """
        When receive delete method, instance won't be deleted from the database.
        Only change is_active field to False
        """

        delete_offer_by_id(offer_id=instance.id)


class InventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Inventory model"""

    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class BalanceViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Balance model"""

    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer


class TradeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Trade model"""

    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
