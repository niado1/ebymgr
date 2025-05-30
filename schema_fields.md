# 📦 Backlog Export CSV Field Summary

This document outlines the fields included in each CSV generated by `generate_backlog_exports()`.

| Field Name       | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| Order ID         | Unique order identifier from eBay                                          |
| Buyer            | Buyer's eBay username                                                      |
| Order Date       | Timestamp the order was placed                                             |
| title            | Full original eBay listing title                                           |
| shortTitle       | Cleaned summary title (redundant keywords removed for readability)         |
| legacyItemId     | eBay legacy item number (used in listing URL)                              |
| categoryId       | eBay category ID for the item                                              |
| listingUrl       | Direct URL to the listing: https://www.ebay.com/itm/<legacyItemId>         |
| itemCost         | Item price extracted from the order                                        |
| daysLate         | Fulfillment urgency flag based on order age: Late, Urgent, HOT             |
| delivered        | Boolean flag indicating if item shows as delivered in Fulfillment API      |
| buyerNote        | Freeform message from buyer entered at checkout                            |
| hasBuyerNote     | Boolean indicating presence of a buyer note                                |
| trackingCount    | Number of tracking records associated with this order                      |
| reship           | Boolean flag indicating if multiple tracking numbers were found (reship?)  |

Each CSV will include relevant rows depending on its filtering logic.

---

Generated: Automatically with each backlog export.
