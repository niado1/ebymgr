import os
import pandas as pd
from datetime import datetime
from picksheet import generate_pick_sheet

def generate_backlog_exports(all_orders):
    df = pd.DataFrame(all_orders)

    # Extract fields from lineItems[0]
    df['title'] = df['lineItems'].apply(lambda items: items[0].get('title', '') if isinstance(items, list) and items else '')
    df['categoryId'] = df['lineItems'].apply(lambda items: items[0].get('categoryId', '') if isinstance(items, list) and items else '')
    df['legacyItemId'] = df['lineItems'].apply(lambda items: items[0].get('legacyItemId', '') if isinstance(items, list) and items else '')
    df['variationAttributes'] = df['lineItems'].apply(
        lambda items: ', '.join(f"{va['name']}: {va['value']}" for va in items[0].get('variationAspects', []))
        if isinstance(items, list) and items and isinstance(items[0], dict) and 'variationAspects' in items[0]
        else ''
    )

    # Ensure required fields exist with default values
    if "buyer" not in df.columns:
        df["buyer"] = []
    if "pricingSummary" not in df.columns:
        df["pricingSummary"] = []
    if "buyerCheckoutNotes" not in df.columns:
        df["buyerCheckoutNotes"] = ''
    if "personalization" not in df.columns:
        df["personalization"] = ''
    if "title" not in df.columns:
        df["title"] = ''
    if "legacyItemId" not in df.columns:
        df["legacyItemId"] = ''
    if "orderDate" not in df.columns:
        df["orderDate"] = pd.NaT
    if "categoryId" not in df.columns:
        df["categoryId"] = ''
    if "itemCost" not in df.columns:
        df["itemCost"] = 0
    if "reship" not in df.columns:
        df["reship"] = ''

    # Merge note fields
    df['note'] = df.apply(lambda row: f"{str(row.get('buyerCheckoutNotes', '')).strip()} | {str(row.get('personalization', '')).strip()}".strip(' |'), axis=1)

    # Extract tracking info from fulfillmentHrefs
    from orders import fetch_tracking_data_from_fulfillment
    tracking_data = fetch_tracking_data_from_fulfillment(df)
    df = df.merge(tracking_data, on='orderId', how='left')

    df["buyerNote"] = df.get("buyerNote", "")

    # Add shortTitle and listingUrl
    df["shortTitle"] = df["title"].astype(str).str.replace(r"[^a-zA-Z0-9 ]", "", regex=True).str.slice(0, 50)
    df["listingUrl"] = "https://www.ebay.com/itm/" + df["legacyItemId"].astype(str)

    # Parse and categorize lateness
    df["orderDate"] = pd.to_datetime(df.get("orderDate", pd.NaT), errors="coerce")

    def categorize_lateness(date):
        if pd.isnull(date):
            return ""
        delta = (datetime.now() - date).days
        if delta > 10:
            return "HOT"
        elif delta > 5:
            return "Urgent"
        elif delta > 3:
            return "Late"
        return ""

    df["daysLate"] = df["orderDate"].apply(categorize_lateness)

    df["categoryId"] = df.get("categoryId", "")
    df["itemCost"] = pd.to_numeric(df.get("itemCost", pd.Series([0] * len(df))), errors="coerce").fillna(0)

    # Send to picksheet generator
    generate_pick_sheet(df.to_dict(orient="records"))
