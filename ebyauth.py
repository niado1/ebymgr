import requests
import base64

# Your eBay credentials
client_id = "JamesTub-ebymgr-PRD-c80007c95-a3394251"
client_secret = "PRD-80007c95863a-ecc2-4231-97f1-dfc1"
redirect_uri = "James_Tubbs-JamesTub-ebymgr-shpoztyr"  # This is your RuName
authorization_code = "v^1.1#i^1#I^3#f^0#p^3#r^1#t^Ul41Xzg6Q0M0NkZFODg3QkU3NTY2OUE4NDYxRTU1OEFDQzJEQjNfMV8x#E^260"

# Encode client_id and secret for the Authorization header
credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {encoded_credentials}",
}

data = {
    "grant_type": "authorization_code",
    "code": authorization_code,
    "redirect_uri": redirect_uri,
}

response = requests.post("https://api.ebay.com/identity/v1/oauth2/token", headers=headers, data=data)

print("Status:", response.status_code)
try:
    result = response.json()
    print("✅ Response:")
    for k, v in result.items():
        print(f"{k}: {v}")
except Exception as e:
    print("❌ Error parsing response:", e)
    print(response.text)
