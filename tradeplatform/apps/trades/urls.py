from apps.registration import views as reg_views
from apps.trades import views as trades_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("currencies", trades_views.CurrencyViewSet)
router.register("items", trades_views.ItemViewSet)
router.register("prices", trades_views.PriceViewSet)
router.register("watchlists", trades_views.WatchListViewSet)
router.register("offers", trades_views.OfferViewSet)
router.register("inventories", trades_views.InventoryViewSet)
router.register("balances", trades_views.BalanceViewSet)
router.register("trades", trades_views.TradeViewSet)
router.register("users", reg_views.UserViewSet)
router.register("userprofiles", reg_views.UserProfileViewSet)

urlpatterns = router.urls
