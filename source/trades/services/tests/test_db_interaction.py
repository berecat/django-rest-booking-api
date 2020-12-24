from trades.models import Offer
from trades.services.db_interaction import (get_all_purchase_active_offers,
                                            get_offer_by_id)


def test_get_all_purchase_active_offers(offer_purchase_instance, offer_sell_instance):
    """Ensure that function correctly give us only offers with PURCHASE status"""

    offers = get_all_purchase_active_offers()

    assert len(offers) == 1
    assert offers[0] == offer_purchase_instance
