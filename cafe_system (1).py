# ============================================================
#   Smart Cafe Inventory & Bill Generation System
#   Team: NeuraTech | Sapthagiri NPS University
#   Members: Jayalakshmi KM, Harshitha Vijay KM,
#            Shreya, Gagana
#   Guide: Dr. B. Vani
# ============================================================

import datetime
import os

# ── Menu ────────────────────────────────────────────────────
MENU = {
    "1": {"name": "Espresso",        "price": 60},
    "2": {"name": "Cappuccino",      "price": 80},
    "3": {"name": "Latte",           "price": 90},
    "4": {"name": "Cold Coffee",     "price": 100},
    "5": {"name": "Masala Chai",     "price": 40},
    "6": {"name": "Green Tea",       "price": 50},
    "7": {"name": "Sandwich",        "price": 70},
    "8": {"name": "Burger",          "price": 120},
    "9": {"name": "Pasta",           "price": 150},
    "10": {"name": "Chocolate Cake", "price": 110},
    "11": {"name": "Muffin",         "price": 60},
    "12": {"name": "French Fries",   "price": 80},
}

GST_RATE = 0.05  # 5%


# ── Display Menu ─────────────────────────────────────────────
def display_menu():
    print("\n" + "=" * 45)
    print("       ☕  SMART CAFE — MENU  ☕")
    print("=" * 45)
    print(f"{'No.':<5} {'Item':<20} {'Price (₹)':>10}")
    print("-" * 45)
    for key, item in MENU.items():
        print(f"{key:<5} {item['name']:<20} {item['price']:>10}")
    print("=" * 45)


# ── Take Order ───────────────────────────────────────────────
def take_order():
    cart = []
    print("\nEnter item number and quantity. Type 'done' when finished.\n")

    while True:
        choice = input("Item number (or 'done'): ").strip()

        if choice.lower() == "done":
            if not cart:
                print("⚠️  Cart is empty! Please add at least one item.")
                continue
            break

        if choice not in MENU:
            print("❌ Invalid item number. Please try again.")
            continue

        try:
            qty = int(input(f"Quantity for {MENU[choice]['name']}: "))
            if qty <= 0:
                print("❌ Quantity must be a positive number.")
                continue
        except ValueError:
            print("❌ Please enter a valid number for quantity.")
            continue

        # Check if item already in cart
        for entry in cart:
            if entry["item_no"] == choice:
                entry["quantity"] += qty
                print(f"✅ Updated {MENU[choice]['name']} → Total qty: {entry['quantity']}")
                break
        else:
            cart.append({
                "item_no":  choice,
                "name":     MENU[choice]["name"],
                "price":    MENU[choice]["price"],
                "quantity": qty,
            })
            print(f"✅ Added {MENU[choice]['name']} x{qty}")

    return cart


# ── Calculate Bill ───────────────────────────────────────────
def calculate_bill(cart):
    subtotal = sum(item["price"] * item["quantity"] for item in cart)
    gst      = round(subtotal * GST_RATE, 2)
    total    = round(subtotal + gst, 2)
    return subtotal, gst, total


# ── Generate Receipt ─────────────────────────────────────────
def generate_receipt(cart, subtotal, gst, total, customer_name):
    timestamp   = datetime.datetime.now()
    receipt_id  = timestamp.strftime("RCP%Y%m%d%H%M%S")
    date_str    = timestamp.strftime("%d-%m-%Y %I:%M %p")

    lines = []
    lines.append("=" * 50)
    lines.append("        ☕  SMART CAFE  ☕")
    lines.append("    Sapthagiri NPS University")
    lines.append("=" * 50)
    lines.append(f"Receipt ID : {receipt_id}")
    lines.append(f"Date/Time  : {date_str}")
    lines.append(f"Customer   : {customer_name}")
    lines.append("-" * 50)
    lines.append(f"{'Item':<22} {'Qty':>4} {'Rate':>8} {'Amount':>10}")
    lines.append("-" * 50)

    for item in cart:
        amount = item["price"] * item["quantity"]
        lines.append(f"{item['name']:<22} {item['quantity']:>4} {item['price']:>8} {amount:>10}")

    lines.append("-" * 50)
    lines.append(f"{'Subtotal':<36} ₹{subtotal:>8.2f}")
    lines.append(f"{'GST (5%)':<36} ₹{gst:>8.2f}")
    lines.append("=" * 50)
    lines.append(f"{'TOTAL AMOUNT':<36} ₹{total:>8.2f}")
    lines.append("=" * 50)
    lines.append("   Thank you for visiting Smart Cafe! 😊")
    lines.append("=" * 50)

    receipt_text = "\n".join(lines)

    # Print to console
    print("\n" + receipt_text)

    # Save to file
    os.makedirs("receipts", exist_ok=True)
    filename = f"receipts/{receipt_id}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(receipt_text)

    print(f"\n📄 Receipt saved → {filename}")
    return receipt_text


# ── Main ─────────────────────────────────────────────────────
def main():
    print("\n" + "=" * 45)
    print("  Welcome to Smart Cafe Inventory System")
    print("         Team NeuraTech 🚀")
    print("=" * 45)

    customer_name = input("\nEnter customer name: ").strip()
    if not customer_name:
        customer_name = "Guest"

    while True:
        display_menu()
        cart              = take_order()
        subtotal, gst, total = calculate_bill(cart)
        generate_receipt(cart, subtotal, gst, total, customer_name)

        again = input("\n🔄 New order? (yes/no): ").strip().lower()
        if again != "yes":
            print("\n👋 Thank you! Goodbye.\n")
            break


if __name__ == "__main__":
    main()
