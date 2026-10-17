import numpy as np
import pandas as pd

# =========================================================
# SETTINGS
# =========================================================

np.random.seed(44)

N = 150000
CUSTOMER_COUNT = 20000

print("Starting Marketing Interactions Dataset...")


# =========================================================
# CUSTOMER IDs
# =========================================================

customer_ids = np.array([
    f"CUST{i:06d}"
    for i in range(1, CUSTOMER_COUNT + 1)
])


# =========================================================
# IDS
# =========================================================

interaction_id = np.array([
    f"MKT{i:09d}"
    for i in range(1, N + 1)
])

customer_id = np.random.choice(
    customer_ids,
    N
)


# =========================================================
# DATE
# =========================================================

interaction_timestamp = pd.to_datetime(
    np.random.randint(
        pd.Timestamp("2025-01-01").value // 10**9,
        pd.Timestamp("2026-10-01").value // 10**9,
        N
    ),
    unit="s"
)


# =========================================================
# CAMPAIGNS
# =========================================================

campaign_name = np.random.choice(
    [
        "Summer Sale",
        "Diwali Offer",
        "New Year Campaign",
        "Festival Discount",
        "Flash Sale",
        "Loyalty Campaign",
        "Product Launch"
    ],
    N
)


# =========================================================
# INTERACTION TYPE
# =========================================================

interaction_type = np.random.choice(
    [
        "Email Sent",
        "Email Opened",
        "Email Clicked",
        "Ad Impression",
        "Ad Clicked",
        "Conversion",
        "Unsubscribe"
    ],
    N,
    p=[
        0.25,
        0.20,
        0.15,
        0.15,
        0.10,
        0.12,
        0.03
    ]
)


# =========================================================
# CHANNEL
# =========================================================

channel = np.random.choice(
    [
        "Email",
        "SMS",
        "Google Ads",
        "Facebook",
        "Instagram",
        "Push Notification"
    ],
    N,
    p=[
        0.30,
        0.15,
        0.20,
        0.12,
        0.13,
        0.10
    ]
)


# =========================================================
# MARKETING COST
# =========================================================

marketing_cost = np.where(
    channel == "Email",
    np.random.uniform(0.05, 1.00, N),
    np.where(
        channel == "SMS",
        np.random.uniform(0.10, 1.50, N),
        np.random.uniform(1.00, 20.00, N)
    )
)


# =========================================================
# CONVERSION REVENUE
# =========================================================

conversion_revenue = np.where(
    interaction_type == "Conversion",
    np.random.uniform(500, 50000, N),
    0
)


# =========================================================
# DATAFRAME
# =========================================================

df = pd.DataFrame({
    "interaction_id": interaction_id,
    "customer_id": customer_id,
    "interaction_timestamp": interaction_timestamp,
    "campaign_name": campaign_name,
    "interaction_type": interaction_type,
    "channel": channel,
    "marketing_cost": np.round(
        marketing_cost,
        2
    ),
    "conversion_revenue": np.round(
        conversion_revenue,
        2
    )
})


# =========================================================
# SAVE
# =========================================================

df.to_csv(
    "C:/Users/hanshika/Desktop/customer-360-intelligence/data/marketing_interactions.csv",
    index=False
)


# =========================================================
# OUTPUT
# =========================================================

print("\nMarketing Interactions Dataset Created!")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nFirst 5 rows:")
print(df.head())

print("\nInteraction counts:")
print(df["interaction_type"].value_counts())

print("\nChannel counts:")
print(df["channel"].value_counts())

print("\nFile created:")
print("marketing_interactions.csv")

print("\nDone!")