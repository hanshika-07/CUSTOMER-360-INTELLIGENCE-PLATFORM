import numpy as np
import pandas as pd

# =========================================================
# SETTINGS
# =========================================================

np.random.seed(42)

N = 35000
CUSTOMER_COUNT = 20000

print("Starting Support Tickets Dataset...")


# =========================================================
# CUSTOMER IDs
# =========================================================

customer_ids = np.array([
    f"CUST{i:06d}"
    for i in range(1, CUSTOMER_COUNT + 1)
])


# =========================================================
# GENERATE BASIC DATA
# =========================================================

ticket_id = np.array([
    f"TICK{i:08d}"
    for i in range(1, N + 1)
])

customer_id = np.random.choice(
    customer_ids,
    N
)

created_date = pd.to_datetime(
    np.random.randint(
        pd.Timestamp("2024-01-01").value // 10**9,
        pd.Timestamp("2026-10-01").value // 10**9,
        N
    ),
    unit="s"
)


# =========================================================
# CATEGORIES
# =========================================================

ticket_category = np.random.choice(
    [
        "Billing",
        "Technical Issue",
        "Product Issue",
        "Delivery",
        "Account"
    ],
    N,
    p=[
        0.20,
        0.25,
        0.20,
        0.20,
        0.15
    ]
)


# =========================================================
# PRIORITY
# =========================================================

priority = np.random.choice(
    [
        "Low",
        "Medium",
        "High",
        "Critical"
    ],
    N,
    p=[
        0.35,
        0.40,
        0.20,
        0.05
    ]
)


# =========================================================
# CHANNEL
# =========================================================

channel = np.random.choice(
    [
        "Email",
        "Phone",
        "Chat",
        "Website",
        "Mobile App"
    ],
    N,
    p=[
        0.25,
        0.20,
        0.25,
        0.15,
        0.15
    ]
)


# =========================================================
# STATUS
# =========================================================

status = np.random.choice(
    [
        "Open",
        "In Progress",
        "Resolved",
        "Closed",
        "Escalated"
    ],
    N,
    p=[
        0.08,
        0.12,
        0.35,
        0.38,
        0.07
    ]
)


# =========================================================
# RESOLUTION TIME
# =========================================================

resolution_time = np.random.randint(
    2,
    168,
    N
).astype(float)

# Open tickets have no resolution time
resolution_time[status == "Open"] = np.nan


# =========================================================
# SATISFACTION SCORE
# =========================================================

satisfaction = np.random.choice(
    [1, 2, 3, 4, 5],
    N,
    p=[
        0.05,
        0.10,
        0.20,
        0.35,
        0.30
    ]
).astype(float)

# Open tickets have no satisfaction score
satisfaction[status == "Open"] = np.nan


# =========================================================
# CREATE DATAFRAME
# =========================================================

df = pd.DataFrame({
    "ticket_id": ticket_id,
    "customer_id": customer_id,
    "created_date": created_date,
    "ticket_category": ticket_category,
    "priority": priority,
    "channel": channel,
    "status": status,
    "resolution_time_hours": resolution_time,
    "satisfaction_score": satisfaction
})


# =========================================================
# SAVE
# =========================================================

df.to_csv(
    "C:/Users/hanshika/Desktop/customer-360-intelligence/data/support_tickets.csv",
    index=False
)


# =========================================================
# OUTPUT
# =========================================================

print("\nSupport Tickets Dataset Created!")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nFirst 5 rows:")
print(df.head())

print("\nFile created:")
print("support_tickets.csv")

print("\nDone!")