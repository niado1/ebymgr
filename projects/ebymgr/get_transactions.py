import requests
from dotenv import load_dotenv
import os

load_dotenv()

APP_ID = os.getenv("EBAY_APP_ID")
DEV_ID = os.getenv("EBAY_DEV_ID")
CERT_ID = os.getenv("EBAY_CERT_ID")
USER_TOKEN = os.getenv("EBAY_USER_TOKEN")

TRADING_API_ENDPOINT = "https://api.ebay.com/ws/api.dll"
HEADERS = {
    "X-EBAY-API-CALL-NAME": "GetItemTransactions",
    "X-EBAY-API-SITEID": "0",
    "X-EBAY-API-APP-NAME": APP_ID,
    "X-EBAY-API-DEV-NAME": DEV_ID,
    "X-EBAY-API-CERT-NAME": CERT_ID,
    "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
    "Content-Type": "text/xml"
}

BODY = f"""<?xml version="1.0" encoding="utf-8"?>
<GetItemTransactionsRequest xmlns="urn:ebay:apis:eBLBaseComponents">
  <RequesterCredentials>
    <eBayAuthToken>{USER_TOKEN}</eBayAuthToken>
  </RequesterCredentials>
  <ItemID>256778865356</ItemID>
  <IncludeFinalValueFee>true</IncludeFinalValueFee>
  <DetailLevel>ReturnAll</DetailLevel>
</GetItemTransactionsRequest>"""

response = requests.post(TRADING_API_ENDPOINT, headers=HEADERS, data=BODY)
print(f"Status Code: {response.status_code}\n")

if response.status_code == 200:
    print("✅ Raw XML response:")
    print(response.text[:3000])  # Trim to avoid explosion
else:
    print("❌ Error fetching transactions.")
    print(response.text)
