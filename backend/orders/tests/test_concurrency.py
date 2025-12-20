from django.db import connection
from rest_framework.test import APIClient # type: ignore
import threading
import pytest # type: ignore


@pytest.mark.django_db(transaction=True)
def test_two_users_cannot_buy_last_unit(
    user,
    another_user,
    product_variant,
):
    product_variant.stock = 1
    product_variant.save()

    results = {}

    def checkout(test_user, key):
        try:
            client = APIClient()
            client.force_authenticate(user=test_user)

            client.post(
                "/api/cart/items/",
                {"variant": product_variant.id, "quantity": 1},
            )
            response = client.post("/api/orders/")
            results[key] = response.status_code
        finally:
            # 🔑 Important: close thread DB connection
            connection.close()

    t1 = threading.Thread(target=checkout, args=(user, "u1"))
    t2 = threading.Thread(target=checkout, args=(another_user, "u2"))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert list(results.values()).count(201) == 1
    assert list(results.values()).count(400) == 1

    product_variant.refresh_from_db()
    assert product_variant.stock == 0
