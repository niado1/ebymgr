
import json
from collections import Counter

with open("raw_orders_with_fulfillments.json", "r", encoding="utf-8") as f:
    orders = json.load(f)

event_type_counter = Counter()
orders_with_events = 0
orders_no_events = 0
total_fulfillments = 0

for order in orders:
    fulfillments = order.get("fulfillments", [])
    for f in fulfillments:
        total_fulfillments += 1
        events = f.get("shipmentTrackingEvents", [])
        if not events:
            orders_no_events += 1
        else:
            orders_with_events += 1
            for e in events:
                event_type = e.get("eventType", "UNKNOWN")
                event_type_counter[event_type] += 1

print(f"📦 Total orders: {len(orders)}")
print(f"🔁 Total fulfillments: {total_fulfillments}")
print(f"✅ Fulfillments with events: {orders_with_events}")
print(f"❌ Fulfillments without events: {orders_no_events}")
print("\n📊 Tracking event types found:")
for event, count in event_type_counter.items():
    print(f"  - {event}: {count}")
