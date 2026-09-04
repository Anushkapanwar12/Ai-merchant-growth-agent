import os
from dotenv import load_dotenv

load_dotenv()


def create_order(amount, receipt, simulate_failure=False):
    """
    Create a Razorpay order.

    Uses MOCK mode when Razorpay credentials are not configured.
    """

    # --------------------------------
    # Validate payment amount
    # --------------------------------

    if amount <= 0:
        raise ValueError(
            "Invalid payment amount. Amount must be greater than zero."
        )

    # --------------------------------
    # Simulate API failure for demo
    # --------------------------------

    if simulate_failure:
        raise RuntimeError(
            "Simulated Razorpay API failure."
        )

    # --------------------------------
    # Load Razorpay credentials
    # --------------------------------

    key_id = os.getenv("RAZORPAY_KEY_ID")
    key_secret = os.getenv("RAZORPAY_KEY_SECRET")

    # --------------------------------
    # MOCK MODE
    # --------------------------------

    if not key_id or not key_secret:

        return {
            "id": f"mock_order_{receipt}",
            "amount": amount,
            "currency": "INR",
            "receipt": receipt,
            "status": "created",
            "mock": True
        }

    # --------------------------------
    # REAL RAZORPAY MODE
    # --------------------------------

    import razorpay

    client = razorpay.Client(
        auth=(key_id, key_secret)
    )

    order = client.order.create(
        data={
            "amount": amount,
            "currency": "INR",
            "receipt": receipt
        }
    )

    return order