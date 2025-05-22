import os
import requests
from dotenv import load_dotenv

load_dotenv()

EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
EBAY_REDIRECT_URI = os.getenv("EBAY_REDIRECT_URI")  # This should be your RuName

def exchange_code_for_tokens(auth_code):
    url = "https://api.ebay.com/identity/v1/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Manually encode form fields without escaping redirect_uri
    payload = (
        f"grant_type=authorization_code"
        f"&code={auth_code}"
        f"&redirect_uri={EBAY_REDIRECT_URI}"
    )

    response = requests.post(
        url,
        headers=headers,
        data=payload,
        auth=(EBAY_CLIENT_ID, EBAY_CLIENT_SECRET),
    )

    if response.ok:
        token_data = response.json()
        print("✅ Token exchange successful.")
        print("Access Token:\n", token_data["access_token"])
        print("Refresh Token:\n", token_data["refresh_token"])

        # Update or append .env with the refresh token
        env_path = ".env"
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        found = False
        with open(env_path, "w", encoding="utf-8") as f:
            for line in lines:
                if line.startswith("EBAY_REFRESH_TOKEN="):
                    f.write(f"EBAY_REFRESH_TOKEN={token_data['refresh_token']}\n")
                    found = True
                else:
                    f.write(line)
            if not found:
                f.write(f"\nEBAY_REFRESH_TOKEN={token_data['refresh_token']}\n")

        print("✅ .env updated with new refresh token.")
    else:
        print("❌ Token exchange failed:")
        print(response.status_code, response.text)

if __name__ == "__main__":
    auth_code = input("Paste your authorization code: ").strip()
    exchange_code_for_tokens(auth_code)
