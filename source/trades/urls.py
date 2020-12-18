from rest_framework import routers

from trades import views

router = routers.DefaultRouter()
router.register('currencies', views.CurrencyViewSet)
router.register('items', views.ItemViewSet)
router.register('prices', views.PriceViewSet)
router.register('watchlists', views.WatchListViewSet)
router.register('offers', views.OfferViewSet)
router.register('inventories', views.InventoryViewSet)
router.register('trades', views.TradeViewSet)

urlpatterns = router.urls