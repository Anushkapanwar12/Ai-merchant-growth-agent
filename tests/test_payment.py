from payments.razorpay_client import create_order


def test_create_order_success():
    """
    Test that a valid payment order is created.
    """

    order = create_order(
        10000,
        "pytest_success_001"
    )

    assert order["amount"] == 10000
    assert order["currency"] == "INR"
    assert order["status"] == "created"
    assert order["mock"] is True


def test_create_order_invalid_amount():
    """
    Test that an invalid payment amount is rejected.
    """

    try:

        create_order(
            0,
            "pytest_invalid_001"
        )

        assert False, "Invalid amount should raise an error."

    except ValueError as e:

        assert "greater than zero" in str(e)