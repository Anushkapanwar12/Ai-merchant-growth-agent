from payments.razorpay_client import create_order


def test_invalid_amount():

    print("\nTesting invalid payment amount...")

    try:

        order = create_order(
            -500,
            "failure_test_001"
        )

        print("❌ Failure test did not trigger.")
        print("Order returned:", order)

    except Exception as e:

        print("✅ Payment failure detected!")
        print("Error:", e)


if __name__ == "__main__":
    test_invalid_amount()