import re

from agent.tools import search_products, get_recommendations


def extract_budget(message):
    """
    Find a budget such as:
    5000
    ₹5000
    under 5000
    below ₹5000
    """

    patterns = [
        r"(?:under|below|within|max(?:imum)?(?: budget)?(?: of)?)\s*₹?\s*(\d[\d,]*)",
        r"₹\s*(\d[\d,]*)"
    ]

    for pattern in patterns:
        match = re.search(pattern, message.lower())

        if match:
            amount = match.group(1).replace(",", "")
            return float(amount)

    return None


def detect_query(message):
    """
    Convert the customer's message into a simple
    product search query.
    """

    message = message.lower()

    if "headphone" in message:
        return "headphones"

    if "earbud" in message:
        return "earbuds"

    if "laptop" in message:
        return "laptop"

    if "keyboard" in message:
        return "keyboard"

    if "mouse" in message:
        return "mouse"

    if "webcam" in message:
        return "webcam"

    if "powerbank" in message or "power bank" in message:
        return "powerbank"

    if "usb" in message or "hub" in message:
        return "hub"

    if "desk mat" in message or "deskmat" in message:
        return "desk"

    if "gaming" in message:
        return "gaming"

    return ""


def format_products(products):
    """
    Convert product results into a readable response.
    """

    if not products:
        return (
            "I couldn't find a matching product. "
            "Try a different search or increase your budget."
        )

    response = "Here are some products I found:\n\n"

    for product in products[:5]:
        response += (
            f"🛍️ **{product['name']}**\n"
            f"💰 ₹{product['price']:,}\n"
            f"📝 {product['description']}\n\n"
        )

    return response


def get_agent_recommendations(user_message):
    """
    Find the main product from the customer's request
    and return complementary products.
    """

    budget = extract_budget(user_message)
    query = detect_query(user_message)

    products = search_products(
        query=query,
        max_price=budget
    )

    if not products:
        return []

    main_product = products[0]

    recommendations = get_recommendations(
        main_product["id"]
    )

    return recommendations


def run_agent(user_message):
    """
    Main shopping-agent function.
    """

    message = user_message.strip()

    if not message:
        return "Please tell me what product you are looking for."

    lower_message = message.lower()

    # General greeting
    if lower_message in ["hello", "hi", "hey"]:
        return (
            "Hello! 👋 I'm your AI shopping assistant.\n\n"
            "I can help you find products, compare prices, "
            "and stay within your budget."
        )

    # Help
    if "what can you do" in lower_message:
        return (
            "I can help you:\n"
            "• 🔎 Search for products\n"
            "• 💰 Find products within your budget\n"
            "• 🛒 Recommend products\n"
            "• 📈 Suggest related products"
        )

    budget = extract_budget(message)
    query = detect_query(message)

    # Search catalog
    products = search_products(
        query=query,
        max_price=budget
    )

    if products:

        response = format_products(products)

        # Find complementary products
        main_product = products[0]

        recommendations = get_recommendations(
            main_product["id"]
        )

        if recommendations:

            response += "\n\n### 💡 You may also like:\n\n"

            for product in recommendations[:2]:

                response += (
                    f"🛍️ **{product['name']}** — "
                    f"₹{product['price']:,}\n"
                )

            response += (
                "\nThese products can complement your "
                "main purchase."
            )

        return response

    if query:

        if budget:
            return (
                f"I couldn't find {query} products under "
                f"₹{budget:,.0f}. Try increasing your budget."
            )

        return f"I couldn't find any {query} products."

    return (
        "I'm not sure what product you're looking for. "
        "Try something like:\n\n"
        "• gaming headphones under ₹5000\n"
        "• laptop under ₹70000\n"
        "• gaming mouse\n"
    )
def get_main_products(user_message):
    """
    Find the main products matching the customer's request.
    """

    budget = extract_budget(user_message)
    query = detect_query(user_message)

    products = search_products(
        query=query,
        max_price=budget
    )

    return products[:1]
