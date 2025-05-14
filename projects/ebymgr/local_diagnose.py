# local_diagnose.py
import json
import requests
from auth import get_access_token

ORDER_IDS = ["27-13003-59198", "15-13000-67100"]
ORDER_ENDPOINT = "https://api.ebay.com/sell/fulfillment/v1/order"

access_token = get_access_token()
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

order_details = {}

for order_id in ORDER_IDS:
    order_url = f"{ORDER_ENDPOINT}/{order_id}"
    order_resp = requests.get(order_url, headers=headers)
    order_data = order_resp.json()

    order_details[order_id] = {
        "order_data": order_data,
        "fulfillments": []
    }

    for href in order_data.get("fulfillmentHrefs", []):
        fulfillment_resp = requests.get(href, headers=headers)
        fulfillment_data = fulfillment_resp.json()
        order_details[order_id]["fulfillments"].append(fulfillment_data)

with open("manual_order_debug.json", "w", encoding="utf-8") as f:
    json.dump(order_details, f, indent=2)

print("✅ Dumped to manual_order_debug.json")
