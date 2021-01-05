from django.urls import path
from rest_framework import routers

from apps.registration import views as reg_views
from apps.trades import views as trades_views

router = routers.DefaultRouter()
router.register("currencies", trades_views.CurrencyViewSet, basename="currency")
router.register("items", trades_views.ItemViewSet, basename="item")
router.register("prices", trades_views.PriceViewSet, basename="price")
router.register("watchlists", trades_views.WatchListViewSet, basename="watchlist")
router.register("offers", trades_views.OfferViewSet, basename="offer")
router.register("inventories", trades_views.InventoryViewSet, basename="inventory")
router.register("balances", trades_views.BalanceViewSet, basename="balance")
router.register("trades", trades_views.TradeViewSet, basename="trade")
router.register("users", reg_views.UserViewSet, basename="user")
router.register("userprofiles", reg_views.UserProfileViewSet, basename="userprofile")
router.register("statistics", trades_views.StatisticView, basename="statistic")

urlpatterns = router.urls
