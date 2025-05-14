def send_messages_to_buyers(orders, message_text):
    for order in orders:
        buyer = order.get("buyer", {}).get("username", "UNKNOWN")
        order_id = order.get("orderId", "N/A")
        print(f"📨 Message to {buyer} (Order #{order_id}):\n{message_text}\n")
    print(f"✅ Sent {len(orders)} messages.")
