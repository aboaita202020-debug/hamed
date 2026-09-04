from app.services.fast_cash import FastCashEngine


def test_recommends_fast_offer_for_website_need():
    engine = FastCashEngine()
    result = engine.recommend({"need": "محتاج موقع"})
    assert result
    assert result[0]["key"] == "landing_page_1_day"
    assert result[0]["guaranteed_revenue"] is False


def test_flash_offer_discount_is_capped():
    engine = FastCashEngine()
    result = engine.flash_offer("starter_store_48h", 20)
    assert result["price"] == 2800.0
    assert result["discount_percent"] == 20


def test_upsell_waits_for_confirmed_payment():
    engine = FastCashEngine()
    assert engine.next_after_confirmed_purchase({"payment_confirmed": False})["ready"] is False
    assert engine.next_after_confirmed_purchase({"payment_confirmed": True})["ready"] is True
