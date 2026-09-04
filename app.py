import streamlit as st
from payments.razorpay_client import create_order
from utils.audit import log_event
from agent.agent import (
    run_agent,
    get_agent_recommendations,
    get_main_products
)
from agent.tools import get_product_by_id


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="AI Merchant Growth Agent",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# Session state
# -----------------------------

if "cart" not in st.session_state:
    st.session_state.cart = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "recommended_products" not in st.session_state:
    st.session_state.recommended_products = []
if "main_products" not in st.session_state:
    st.session_state.main_products = []

if "cross_sell_ids" not in st.session_state:
    st.session_state.cross_sell_ids = set()
# -----------------------------
# Helper functions
# -----------------------------

def add_product(product_id):
    product = get_product_by_id(product_id)

    if product is None:
        return False

    st.session_state.cart.append(product)

    return True


def remove_product(index):
    if 0 <= index < len(st.session_state.cart):
        st.session_state.cart.pop(index)


def calculate_total():
    return sum(
        product["price"]
        for product in st.session_state.cart
    )


# -----------------------------
# Header
# -----------------------------

st.title("🤖 AI Merchant Growth Agent")

st.write(
    "An AI-powered shopping assistant that helps customers "
    "discover products and helps merchants grow sales."
)


# -----------------------------
# AI Shopping Assistant
# -----------------------------

st.header("💬 AI Shopping Assistant")

st.write(
    "Ask me what you want to buy, and I will recommend "
    "products from the store catalog."
)


# -----------------------------
# Chat history
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# Chat input
# -----------------------------

user_message = st.chat_input(
    "Example: I need gaming headphones under ₹5000"
)


if user_message:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # Get AI response
    response = run_agent(user_message)

    # Find main product
    st.session_state.main_products = (
        get_main_products(user_message)
    )

    # Find complementary products
    st.session_state.recommended_products = (
        get_agent_recommendations(user_message)
    )

    # Save AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    st.rerun()
# -----------------------------
# Main Product
# -----------------------------

if st.session_state.main_products:

    st.divider()

    st.header("🛍️ Main Product")

    for product in st.session_state.main_products:

        st.subheader(product["name"])

        st.write(product["description"])

        st.write(
            f"### ₹{product['price']:,}"
        )

        if st.button(
            f"🛒 Add {product['name']}",
            key=f"main_{product['id']}"
        ):

            success = add_product(product["id"])

            if success:

                st.success(
                    f"{product['name']} added to cart!"
                )
# -----------------------------
# Recommended products
# -----------------------------

if st.session_state.recommended_products:

    st.divider()

    st.header("💡 Recommended Products")

    st.write(
        "Add complementary products directly to your cart."
    )

    for index, product in enumerate(
        st.session_state.recommended_products
    ):

        st.subheader(product["name"])

        st.write(product["description"])

        st.write(
            f"### ₹{product['price']:,}"
        )

        if st.button(
            f"🛒 Add {product['name']}",
            key=f"recommend_{product['id']}_{index}"
        ):

            success = add_product(product["id"])

            if success:

                st.session_state.cross_sell_ids.add(
                    product["id"]
                )

                st.success(
                    f"{product['name']} added to cart!"
                )

            else:

                st.error(
                    "Product could not be added."
                )
# -----------------------------
# Cart
# -----------------------------

st.header("🛒 Your Cart")

if st.session_state.cart:

    for index, product in enumerate(st.session_state.cart):

        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(
                f"**{product['name']}** — "
                f"₹{product['price']:,}"
            )

        with col2:

            if st.button(
                "Remove",
                key=f"remove_{index}"
            ):

                removed_product = (
                    st.session_state.cart[index]
                )

                st.session_state.cross_sell_ids.discard(
                    removed_product["id"]
                )

                remove_product(index)

                st.rerun()

    st.divider()

    total = calculate_total()

    st.subheader(
        f"💰 Total: ₹{total:,}"
    )

    # -----------------------------
    # Human Approval / Safety Gate
    # -----------------------------

    st.subheader("🔐 Payment Approval")

    st.warning(
        "The AI agent cannot create a payment automatically. "
        "Please review and approve the order yourself."
    )

    approval = st.checkbox(
        f"I approve the payment of ₹{total:,}",
        key="payment_approval"
    )
    simulate_failure = st.checkbox(
        "🧪 Simulate payment failure",
        key="simulate_payment_failure"
    )
    if st.button(
            "✅ Approve & Create Payment Order",
            disabled=not approval
        ):

        # -----------------------------
        # Audit: Human Approval
        # -----------------------------

        log_event(
            "USER_APPROVAL",
            {
                "amount": total,
                "currency": "INR",
                "items": [
                    product["id"]
                    for product in st.session_state.cart
                ]
            }
        )

        try:

            # -----------------------------
            # Convert rupees to paise
            # -----------------------------

            amount_paise = total * 100

            # -----------------------------
            # Create Razorpay order
            # -----------------------------

            order = create_order(
    amount_paise,
    f"cart_{st.session_state.get('order_counter', 0) + 1}",
    simulate_failure=simulate_failure
)

            # -----------------------------
            # Update order counter
            # -----------------------------

            st.session_state.order_counter = (
                st.session_state.get("order_counter", 0) + 1
            )

            # -----------------------------
            # Audit: Order Created
            # -----------------------------

            log_event(
                "ORDER_CREATED",
                {
                    "order_id": order["id"],
                    "amount": total,
                    "currency": order["currency"],
                    "mock": order.get("mock", False)
                }
            )

            # -----------------------------
            # Success message
            # -----------------------------

            st.success(
                "Payment order created successfully!"
            )

            st.write("### Order Details")

            st.write(
                f"**Order ID:** `{order['id']}`"
            )

            st.write(
                f"**Amount:** ₹{total:,}"
            )

            st.write(
                f"**Currency:** {order['currency']}"
            )

            if order.get("mock"):

                st.info(
                    "🧪 Test Mode: This is a simulated Razorpay order. "
                    "No real money has been charged."
                )

        except Exception as e:

            # -----------------------------
            # Audit: Order Creation Failed
            # -----------------------------

            log_event(
                "ORDER_FAILED",
                {
                    "amount": total,
                    "currency": "INR",
                    "error": str(e)
                }
            )

            # -----------------------------
            # Show failure to user
            # -----------------------------

            st.error(
                "❌ Payment order could not be created."
            )

            st.warning(
                "No payment was processed. "
                "You can review the cart and safely retry."
            )

            st.write(
                f"**Reason:** {str(e)}"
            )
else:

    st.info("Your cart is empty.")
# -----------------------------
# Merchant Growth Dashboard
# -----------------------------

st.divider()

st.header("📈 Merchant Growth Dashboard")

st.write(
    "Track how AI recommendations can increase "
    "customer basket value."
)

cart_value = calculate_total()

items_in_cart = len(
    st.session_state.cart
)

cross_sell_products = [
    product
    for product in st.session_state.cart
    if product["id"] in st.session_state.cross_sell_ids
]

cross_sell_revenue = sum(
    product["price"]
    for product in cross_sell_products
)

cross_sell_count = len(
    cross_sell_products
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Cart Value",
        f"₹{cart_value:,}"
    )

with col2:
    st.metric(
        "🛒 Items in Cart",
        items_in_cart
    )

with col3:
    st.metric(
        "📈 Cross-sell Revenue",
        f"₹{cross_sell_revenue:,}"
    )

with col4:
    st.metric(
        "🎯 Cross-sell Items",
        cross_sell_count
    )