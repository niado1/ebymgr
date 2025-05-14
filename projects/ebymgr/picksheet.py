import os
import pandas as pd
from datetime import datetime
from openpyxl import Workbook

FILTER_DIR = "filter_history"
os.makedirs(FILTER_DIR, exist_ok=True)

def generate_pick_sheet(orders, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    df = pd.DataFrame(orders)

    # Fill missing fields with safe defaults
    df["shortTitle"] = df.get("shortTitle", "")
    df["listingUrl"] = df.get("listingUrl", "")
    df["variationAttributes"] = df.get("variationAttributes", "")
    df["trackingNumber"] = df.get("trackingNumber", "")
    df["shippingService"] = df.get("shippingService", "")
    df["trackingStatus"] = df.get("trackingStatus", "")
    df["categoryId"] = df.get("categoryId", "")
    df["itemCost"] = df.get("itemCost", 0)
    df["daysLate"] = df.get("daysLate", "")
    df["reship"] = df.get("reship", False)

    df["note"] = df.get("note", "")

    # Define output columns
    output_columns = [
        "shortTitle",
        "listingUrl",
        "variationAttributes",
        "trackingNumber",
        "shippingService",
        "trackingStatus",
        "categoryId",
        "itemCost",
        "daysLate",
        "reship",
        "note",
    ]

    # Ensure clean formatting
    df["itemCost"] = pd.to_numeric(df["itemCost"], errors="coerce").fillna(0)

    # Filtered sheets
    sheets = {
        "hot": df[df["daysLate"] == "HOT"],
        "reships": df[df["reship"] == True],
        "notes": df[df["note"].str.strip() != ""],
        "delivered": df[df["trackingStatus"] == "Delivered"],
    }

    for label, sub_df in sheets.items():
        path = os.path.join(FILTER_DIR, f"pick_sheet_{label}_{timestamp}.xlsx")
        sub_df.to_excel(path, index=False, columns=output_columns)
        print(f"✅ Exported: {path}")

    # Full sheet as CSV (including all columns for raw ref)
    csv_path = os.path.join(FILTER_DIR, f"pick_sheet_full_{timestamp}.csv")
    df.to_csv(csv_path, index=False)
    print(f"✅ Exported: {csv_path}")
