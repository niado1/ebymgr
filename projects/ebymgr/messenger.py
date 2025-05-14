import requests
from config import EBAY_BASE_URL
from auth import get_access_token

def send_message(buyer_username, subject, body):
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    url = f"{EBAY_BASE_URL}/commerce/notification/v1/public_message"  # Placeholder endpoint; adjust if needed

    payload = {
        "to": buyer_username,
        "subject": subject,
        "message": body
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        print(f"✅ Message sent to {buyer_username}")
    else:
        print(f"❌ Failed to send message to {buyer_username}: {response.text}")

def send_bulk_messages(pick_sheet_path, subject_template, body_template):
    import pandas as pd
    df = pd.read_csv(pick_sheet_path)
    for _, row in df.iterrows():
        subject = subject_template.format(**row)
        body = body_template.format(**row)
        send_message(row['Buyer Username'], subject, body)
