from agent.agent import (
    get_main_products,
    get_agent_recommendations
)


def test_main_product_search():
    """
    Test that the agent can find a main product.
    """

    products = get_main_products(
        "I need gaming headphones under 5000"
    )

    assert len(products) > 0
    assert products[0]["id"] == "P001"


def test_agent_recommendations():
    """
    Test that complementary products are recommended.
    """

    recommendations = get_agent_recommendations(
        "I need gaming headphones under 5000"
    )

    assert len(recommendations) > 0

    recommendation_ids = [
        product["id"]
        for product in recommendations
    ]

    assert "P002" in recommendation_ids
    assert "P003" in recommendation_ids