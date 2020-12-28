from django.contrib import admin

from apps.trades.models import (Balance, Currency, Inventory, Item, Offer,
                                Price, Trade, WatchList)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    list_filter = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("code",)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    list_filter = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("code",)


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ("currency", "item", "price", "date")
    list_filter = (
        "price",
        "date",
        "item__code",
    )
    search_fields = (
        "item__code",
        "price",
    )
    ordering = ("-price", "item__code")


@admin.register(WatchList)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("user",)
    list_filter = ("user__username",)
    search_fields = ("user__username",)
    ordering = ("user__username",)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "status",
        "entry_quantity",
        "price",
        "is_active",
    )
    list_filter = (
        "user__username",
        "status",
        "is_active",
    )
    search_fields = (
        "user__username",
        "status",
        "entry_quantity",
        "price",
    )
    ordering = (
        "-price",
        "-entry_quantity",
    )


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "item",
        "quantity",
    )
    list_filter = (
        "user__username",
        "item__code",
    )
    search_fields = (
        "user__username",
        "item__code",
        "quantity",
    )
    ordering = (
        "user__username",
        "item__code",
        "-quantity",
    )


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "currency",
        "quantity",
    )
    list_filter = (
        "user__username",
        "currency__code",
    )
    search_fields = (
        "user__username",
        "currency__code",
        "quantity",
    )
    ordering = (
        "user__username",
        "currency__code",
        "-quantity",
    )


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = (
        "item",
        "seller",
        "buyer",
        "quantity",
        "unit_price",
        "buyer_offer",
        "seller_offer",
    )
    list_filter = (
        "item__code",
        "seller__username",
        "buyer__username",
    )
    search_fields = (
        "item__code",
        "seller__username",
        "buyer__username",
        "unit__price",
        "quantity",
    )
    ordering = (
        "item__code",
        "-unit_price",
        "-quantity",
    )
