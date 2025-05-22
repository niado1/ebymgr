import json
import requests
import pandas as pd
import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

def get_access_token():
    # Load credentials and refresh token from .env file
    client_id = os.getenv('EBAY_CLIENT_ID')
    client_secret = os.getenv('EBAY_CLIENT_SECRET')
    refresh_token = os.getenv('EBAY_REFRESH_TOKEN')

    # Prepare the request for the OAuth token
    url = "https://api.ebay.com/identity/v1/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {requests.auth._basic_auth_str(client_id, client_secret)}"
    }
    body = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": "https://api.ebay.com/oauth/api_scope"  # Adjust scope as necessary
    }

    # Make the request for a new access token
    response = requests.post(url, headers=headers, data=body)
    response_data = response.json()

    if response.status_code != 200:
        logger.error("Failed to retrieve access token: %s", response_data)
        raise Exception("Failed to retrieve access token")

    return response_data['access_token']

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
    """Extract trackingNumber, shippingService, trackingStatus from fulfillment data."""
    results = []

    for _, row in df.iterrows():
        order_id = row.get("orderId")
        fulfillments = row.get("fulfillmentStartInstructions", [])
        tracking_number = ""
        shipping_service = ""
        tracking_status = ""

        if isinstance(fulfillments, list) and len(fulfillments) > 0:
            for f in fulfillments:
                try:
                    shipment = f.get("shippingStep", {}).get("shipmentTracking", {})
                    tracking_number = shipment.get("trackingNumber", "") or tracking_number
                    shipping_service = shipment.get("shippingCarrierCode", "") or shipping_service
                    tracking_status = shipment.get("status", "") or tracking_status
                except Exception:
                    continue

        results.append({
            "orderId": order_id,
            "trackingNumber": tracking_number,
            "shippingService": shipping_service,
            "trackingStatus": tracking_status
        })

    return pd.DataFrame(results)