from orders import get_orders_raw
from picksheet import generate_pick_sheet
from messaging import send_messages_to_buyers
import pandas as pd
from datetime import datetime, timedelta
import os

def filter_by_date(order, days):
    try:
        cutoff = datetime.utcnow() - timedelta(days=days)
        created = datetime.strptime(order["creationDate"][:19], "%Y-%m-%dT%H:%M:%S")
        return created >= cutoff
    except:
        return False

def filter_by_status(order, status):
    return order.get("orderFulfillmentStatus", "").upper() == status.upper()

def filter_by_username(order, users):
    username = order.get("buyer", {}).get("username", "").lower()
    return username in [u.lower() for u in users]

def filter_has_note(order):
    note = order.get("buyerCheckoutNotes", "")
    return bool(note and note.strip())

def filter_by_sku(order, keywords):
    items = order.get("lineItems", [])
    for item in items:
        sku = item.get("sku", "").lower()
        title = item.get("title", "").lower()
        if any(k in sku or k in title for k in keywords):
            return True
    return False

def filter_unscanned(order):
    fulfillments = order.get("fulfillments", [])
    if not fulfillments:
        return False
    for f in fulfillments:
        events = f.get("shipmentTrackingEvents", [])
        if any(e.get("eventType", "").lower() in ["delivered", "in_transit"] for e in events):
            return False
    return True
if __name__ == "__main__":
    print("🧮 Fetching all orders...")
    all_orders = get_orders_raw()

    print("🔧 Choose filters to apply:")
    print("1. Order age (last N days)")
    print("2. Fulfillment status")
    print("3. Buyer username")
    print("4. Orders with buyer notes")
    print("5. Match SKU or title keywords")
    print("6. No filters (show everything)")
    print("7. Orders with tracking but no scan")
    print("8. Generate backlog analysis & multi-sheet export")

    choices = input("Enter choices (e.g. 1,3,5): ").strip().split(",")


    if "8" in choices:
        from backlog_export import generate_backlog_exports
        generate_backlog_exports(all_orders)
        exit()
    filters = []
    label_parts = []

    if "1" in choices:
        days = int(input("📆 Enter how many days back to include: "))
        filters.append(lambda o: filter_by_date(o, days))
        label_parts.append(f"days={days}")
    if "2" in choices:
        status = input("🚚 Enter fulfillment status (e.g. IN_PROGRESS, FULFILLED): ")
        filters.append(lambda o: filter_by_status(o, status))
        label_parts.append(f"status={status}")
    if "3" in choices:
        users = input("👤 Enter comma-separated usernames: ").split(",")
        users = [u.strip() for u in users if u.strip()]
        filters.append(lambda o: filter_by_username(o, users))
        label_parts.append(f"user_count={len(users)}")
    if "4" in choices:
        filters.append(filter_has_note)
        label_parts.append("has_note")
    if "5" in choices:
        skus = input("🔍 Enter SKU/title keywords (comma-separated): ").split(",")
        skus = [k.strip().lower() for k in skus if k.strip()]
        filters.append(lambda o: filter_by_sku(o, skus))
        label_parts.append(f"sku_count={len(skus)}")
    if "7" in choices:
        filters.append(filter_unscanned)
        label_parts.append("unscanned")

    if not filters or "6" in choices:
        filtered = all_orders
        label_parts.append("all")
    else:
        def combined(o): return all(f(o) for f in filters)
        filtered = [o for o in all_orders if combined(o)]

    print(f"✅ {len(filtered)} orders matched.")

    os.makedirs("filter_history", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    label = "_".join(label_parts)
    filename = f"filter_history/pick_sheet_{label}_{timestamp}.csv"

    generate_pick_sheet(filtered, output_file=filename)

    df = pd.read_csv(filename)
    if df.empty:
        print("🕳️ No orders to message.")
    else:
        send = input("✉️ Send messages to buyers from pick sheet? (y/n): ").strip().lower()
        if send == "y":
            message = input("📝 Enter message to send:\n> ")
            for _, row in df.iterrows():
                print(f"📨 Message to {row.get('Buyer Username')}: {message}")