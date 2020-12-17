from rest_framework import (mixins,
                            viewsets)

from trades.models import (Currency,
                           Item,
                           Price,
                           WatchList,
                           Offer,
                           Inventory,
                           Trade)
from trades.serializers import (CurrencySerializer,
                                ItemSerializer,
                                PriceSerializer,
                                WatchListSerializer,
                                OfferSerializer,
                                InventorySerializer,
                                TradeSerializer)


class CurrencyViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """ViewSet for Currency model"""

    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class ItemViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """ViewSet for Item model"""

    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class PriceViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """ViewSet for Price model"""

    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class WatchListViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    """ViewSet for WatchList model"""

    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer


class OfferViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """ViewSet for Offer model"""

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class InventoryViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    """ViewSet for Inventory model"""

    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class TradeViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """ViewSet for Trade model"""

    queryset = Trade.objects.all()
    serializer_class = TradeSerializer