import os
import pandas as pd
from datetime import datetime
from picksheet import generate_pick_sheet

def generate_backlog_exports(all_orders):
    df = pd.DataFrame(all_orders)

    # Safely access 'lineItems' and other fields
    df['title'] = df.apply(lambda row: row['lineItems'][0].get('title', '') if 'lineItems' in row and isinstance(row['lineItems'], list) and row['lineItems'] else '', axis=1)
    df['categoryId'] = df.apply(lambda row: row['lineItems'][0].get('categoryId', '') if 'lineItems' in row and isinstance(row['lineItems'], list) and row['lineItems'] else '', axis=1)
    df['legacyItemId'] = df.apply(lambda row: row['lineItems'][0].get('legacyItemId', '') if 'lineItems' in row and isinstance(row['lineItems'], list) and row['lineItems'] else '', axis=1)
    df['variationAttributes'] = df.apply(
        lambda row: ', '.join(f"{va['name']}: {va['value']}" for va in row['lineItems'][0].get('variationAspects', []))
        if 'lineItems' in row and isinstance(row['lineItems'], list) and row['lineItems'] and isinstance(row['lineItems'][0], dict) and 'variationAspects' in row['lineItems'][0]
        else '', axis=1
    )

    # Ensure required fields exist with default values
    for field in ["buyer", "pricingSummary", "buyerCheckoutNotes", "personalization", "title", "legacyItemId", "orderDate", "categoryId", "itemCost", "reship"]:
        if field not in df.columns:
            df[field] = '' if df.dtypes.get(field, pd.Series(dtype='object')).name in ['object', 'str'] else pd.NaT

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