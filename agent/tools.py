import json
from pathlib import Path


# Find the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Location of our product catalog
PRODUCTS_FILE = PROJECT_ROOT / "data" / "products.json"


def load_products():
    """Load all products from products.json."""
    
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def search_products(query="", max_price=None, category=None):
    """
    Search products using a text query, maximum price, and category.
    """

    products = load_products()
    results = []

    query = query.lower().strip()

    for product in products:

        # Combine searchable information
        searchable_text = (
            product["name"] + " "
            + product["category"] + " "
            + product["description"] + " "
            + " ".join(product["tags"])
        ).lower()

        # Check query
        query_matches = (
            not query
            or all(word in searchable_text for word in query.split())
        )

        # Check price
        price_matches = (
            max_price is None
            or product["price"] <= max_price
        )

        # Check category
        category_matches = (
            category is None
            or product["category"].lower() == category.lower()
        )

        if query_matches and price_matches and category_matches:
            results.append(product)

    return results
# -----------------------------
# Shopping Cart
# -----------------------------

cart = []


def get_product_by_id(product_id):
    """Find a product using its ID."""

    products = load_products()

    for product in products:
        if product["id"] == product_id:
            return product

    return None


def add_to_cart(product_id):
    """Add a product to the shopping cart."""

    product = get_product_by_id(product_id)

    if product is None:
        return {
            "success": False,
            "message": "Product not found."
        }

    cart.append(product)

    return {
        "success": True,
        "message": f"{product['name']} added to cart.",
        "product": product
    }


def remove_from_cart(product_id):
    """Remove a product from the shopping cart."""

    for i, product in enumerate(cart):

        if product["id"] == product_id:
            removed = cart.pop(i)

            return {
                "success": True,
                "message": f"{removed['name']} removed from cart."
            }

    return {
        "success": False,
        "message": "Product is not in the cart."
    }


def view_cart():
    """Return all products currently in the cart."""

    return cart


def calculate_total():
    """Calculate the total price of all products in the cart."""

    total = sum(product["price"] for product in cart)

    return total
def get_recommendations(product_id, max_price=None):
    """
    Return complementary products for a given product.
    """

    product = get_product_by_id(product_id)

    if product is None:
        return []

    recommendations = []

    for recommended_id in product.get("complements", []):

        recommended_product = get_product_by_id(
            recommended_id
        )

        if recommended_product is None:
            continue

        if (
            max_price is not None
            and recommended_product["price"] > max_price
        ):
            continue

        recommendations.append(
            recommended_product
        )

    return recommendations