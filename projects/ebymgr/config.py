import os
from dotenv import load_dotenv

load_dotenv()

# Credentials (from .env or set manually here)
EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
EBAY_REFRESH_TOKEN = os.getenv("EBAY_REFRESH_TOKEN")

# eBay endpoints
EBAY_BASE_URL = "https://api.ebay.com"
EBAY_AUTH_URL = f"{EBAY_BASE_URL}/identity/v1/oauth2/token"
EBAY_ORDERS_ENDPOINT = f"{EBAY_BASE_URL}/sell/fulfillment/v1/order"
EBAY_MESSAGE_ENDPOINT = f"{EBAY_BASE_URL}/post-order/v2/inquiry"
