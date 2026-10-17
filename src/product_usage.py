import numpy as np
import pandas as pd

# =========================================================
# SETTINGS
# =========================================================

np.random.seed(43)

N = 300000
CUSTOMER_COUNT = 20000

print("Starting Product Usage Events Dataset...")


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

event_id = np.array([
    f"EVT{i:09d}"
    for i in range(1, N + 1)
])

customer_id = np.random.choice(
    customer_ids,
    N
)


# =========================================================
# TIMESTAMP
# =========================================================

event_timestamp = pd.to_datetime(
    np.random.randint(
        pd.Timestamp("2025-01-01").value // 10**9,
        pd.Timestamp("2026-10-01").value // 10**9,
        N
    ),
    unit="s"
)


# =========================================================
# EVENT TYPE
# =========================================================

event_type = np.random.choice(
    [
        "Login",
        "Logout",
        "Product View",
        "Search",
        "Add to Cart",
        "Purchase"
    ],
    N,
    p=[
        0.30,
        0.15,
        0.25,
        0.15,
        0.10,
        0.05
    ]
)


# =========================================================
# DEVICE
# =========================================================

device_type = np.random.choice(
    [
        "Mobile",
        "Desktop",
        "Tablet"
    ],
    N,
    p=[
        0.55,
        0.35,
        0.10
    ]
)


# =========================================================
# OPERATING SYSTEM
# =========================================================

operating_system = np.random.choice(
    [
        "Android",
        "iOS",
        "Windows",
        "macOS",
        "Linux"
    ],
    N,
    p=[
        0.40,
        0.20,
        0.25,
        0.10,
        0.05
    ]
)


# =========================================================
# SESSION DATA
# =========================================================

session_duration_seconds = np.random.randint(
    5,
    3600,
    N
)

pages_viewed = np.random.randint(
    1,
    30,
    N
)


# =========================================================
# DATAFRAME
# =========================================================

df = pd.DataFrame({
    "event_id": event_id,
    "customer_id": customer_id,
    "event_timestamp": event_timestamp,
    "event_type": event_type,
    "device_type": device_type,
    "operating_system": operating_system,
    "session_duration_seconds": session_duration_seconds,
    "pages_viewed": pages_viewed
})


# =========================================================
# SAVE
# =========================================================

df.to_csv(
    "C:/Users/hanshika/Desktop/customer-360-intelligence/data/product_usage_events.csv",
    index=False
)


# =========================================================
# OUTPUT
# =========================================================

print("\nProduct Usage Events Dataset Created!")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nFirst 5 rows:")
print(df.head())

print("\nEvent counts:")
print(df["event_type"].value_counts())

print("\nFile created:")
print("product_usage_events.csv")

print("\nDone!")