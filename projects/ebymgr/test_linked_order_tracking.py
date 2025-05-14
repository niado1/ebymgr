import requests
from auth import get_access_token
import json

FULFILLMENT_API_ENDPOINT = "https://api.ebay.com/sell/fulfillment/v1/order"
access_token = get_access_token()

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

params = {
    "limit": 50
}

response = requests.get(FULFILLMENT_API_ENDPOINT, headers=headers, params=params)
print(f"Status Code: {response.status_code}\n")

if response.status_code == 200:
    orders = response.json().get("orders", [])
    found = 0
    for order in orders:
        for item in order.get("lineItems", []):
            linked = item.get("linkedOrderLineItems", [])
            if linked:
                found += 1
                print("🧩 Linked Line Items Found:")
                print(json.dumps(linked, indent=2))
    if found == 0:
        print("🚫 No linkedOrderLineItems found in sample.")
else:
    print("❌ Error pulling orders:")
    print(response.text)
