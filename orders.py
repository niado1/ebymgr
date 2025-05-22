# === Corrected Version: orders.py ===
import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
EBAY_REFRESH_TOKEN = os.getenv("EBAY_REFRESH_TOKEN")
EBAY_AUTH_URL = "https://api.ebay.com/identity/v1/oauth2/token"

def get_access_token():
    """Obtain a fresh eBay access token using the long-term refresh token."""
    credentials = f"{EBAY_CLIENT_ID}:{EBAY_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}"
    }
    
    data = {
        "grant_type": "refresh_token",
        "refresh_token": EBAY_REFRESH_TOKEN,
        "scope": "https://api.ebay.com/oauth/api_scope/sell.fulfillment"
    }

    response = requests.post(EBAY_AUTH_URL, headers=headers, data=data)
    if response.ok:
        print("✅ Access token retrieved.")
        return response.json()["access_token"]
    else:
        print("❌ Failed to get access token:")
        print(response.status_code, response.text)
        raise Exception("Failed to retrieve access token")

def get_orders_raw():
    token = get_access_token()
    # Placeholder for additional code to fetch orders using the token
    # This part of the code would typically involve setting up another request
    # to an eBay API endpoint that handles orders, using the access token in the
    # Authorization header.
    print("Token for orders:", token)

# Example usage
if __name__ == "__main__":
    get_orders_raw()