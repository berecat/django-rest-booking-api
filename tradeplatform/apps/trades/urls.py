from apps.trades import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("currencies", views.CurrencyViewSet)
router.register("items", views.ItemViewSet)
router.register("prices", views.PriceViewSet)
router.register("watchlists", views.WatchListViewSet)
router.register("offers", views.OfferViewSet)
router.register("inventories", views.InventoryViewSet)
router.register("balances", views.BalanceViewSet)
router.register("trades", views.TradeViewSet)

urlpatterns = router.urls
