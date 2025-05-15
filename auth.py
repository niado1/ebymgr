import base64
import requests
from config import (
    EBAY_CLIENT_ID,
    EBAY_CLIENT_SECRET,
    EBAY_REFRESH_TOKEN,
    EBAY_AUTH_URL,
)

def get_access_token():
    """Obtain a fresh eBay access token using the long-term refresh token."""
    credentials = f"{EBAY_CLIENT_ID}:{EBAY_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}",
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": EBAY_REFRESH_TOKEN,
        "scope": "https://api.ebay.com/oauth/api_scope/sell.fulfillment",
    }

    response = requests.post(EBAY_AUTH_URL, headers=headers, data=data)

    if response.ok:
        access_token = response.json().get("access_token")
        print("✅ Access token retrieved.")
        return access_token
    else:
        print("❌ Failed to get access token:")
        print(response.status_code, response.text)
        return None
