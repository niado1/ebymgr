import json
import requests
import pandas as pd
import logging
from auth import get_access_token

logger = logging.getLogger(__name__)

def get_orders_raw():
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = "https://api.ebay.com/sell/fulfillment/v1/order?limit=200"

    response = requests.get(url, headers=headers)
    orders = response.json().get("orders", [])

    with open("raw_orders.json", "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=2)

    # Also save with fulfillment for later debugging
    for o in orders:
        if "fulfillmentHrefs" in o:
            o["fulfillmentHrefsCount"] = len(o["fulfillmentHrefs"])
    with open("raw_orders_with_fulfillments.json", "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=2)

    logging.info("Fetched %d orders from eBay API", len(orders))
    return orders


def fetch_tracking_data_from_fulfillment(df):
    tracking_rows = []
    for _, row in df.iterrows():
        order_id = row.get('orderId')
        tracking_info = {
            'orderId': order_id,
            'trackingNumber': '',
            'shippingService': '',
            'trackingStatus': 'Unscanned'
        }

        fulfillments = row.get('fulfillmentStartInstructions', [])
        if isinstance(fulfillments, list) and fulfillments:
            for f in fulfillments:
                if 'shippingStep' in f and 'shipTo' in f['shippingStep']:
                    carrier = f.get('shippingStep', {}).get('shippingCarrierCode', '')
                    service = f.get('shippingStep', {}).get('shippingServiceCode', '')
                    tracking = f.get('shippingStep', {}).get('shipmentTrackingNumber', '')

                    if tracking:
                        tracking_info['trackingNumber'] = tracking
                        tracking_info['shippingService'] = service
                        tracking_info['trackingStatus'] = 'In Transit'
                        break

        tracking_rows.append(tracking_info)

    return pd.DataFrame(tracking_rows)
