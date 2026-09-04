# AI Merchant Growth Agent

An AI-powered shopping assistant that helps customers discover relevant products while helping merchants increase basket value through intelligent recommendations and cross-selling.

Built for the **Razorpay AI Buildathon — AI Growth & Agentic Commerce** track.

---

## Project Overview

The AI Merchant Growth Agent acts as a conversational shopping assistant.

Instead of simply searching for products, the agent:

1. Understands what the customer wants.
2. Finds a suitable main product.
3. Recommends complementary products.
4. Adds selected products to a shopping cart.
5. Calculates the basket value.
6. Requests explicit human approval before creating a payment order.
7. Creates a Razorpay-compatible simulated payment order in safe mock mode.
8. Records important actions in an audit log.
9. Handles payment failures safely without processing a payment.

The goal is to demonstrate how AI can increase merchant sales while keeping financial actions **bounded, explainable, auditable, and human-gated**.
> **Payment Integration Note:**  
> This project currently uses a safe mock payment mode because no Razorpay account or API credentials are configured. No real money is charged. The payment flow demonstrates human approval, amount validation, audit logging, and failure recovery without storing or exposing payment credentials.
---

# Problem

Traditional online shopping experiences often rely on:

- Keyword-based product search
- Static recommendations
- Manual product discovery
- Limited contextual cross-selling

This can lead to missed opportunities for both customers and merchants.

For example, a customer searching for a gaming laptop may also need:

- A laptop stand
- A USB-C hub
- A mouse
- Other complementary accessories

The system should be able to identify these opportunities without automatically making financial decisions on behalf of the customer.

---

# Solution

The AI Merchant Growth Agent combines:

**Conversational AI + Product Search + Recommendations + Cross-selling + Human-Gated Payments + Audit Logging + Failure Recovery**

### Example

Customer:

> I need a laptop for coding under ₹70,000.

The agent searches the catalog and identifies a suitable laptop.

It can then recommend complementary products such as:

- Laptop stand
- USB-C hub

The customer chooses what to add to the cart.

Before payment:

> The AI agent cannot create a payment automatically. Please review and approve the order yourself.

The customer must explicitly approve the payment.

---

# Key Features

## 1. AI Shopping Assistant

Customers can describe what they want using natural language.

Example:

```text
I need gaming headphones under ₹5000