import numpy as np
import pandas as pd

# =========================================================
# SETTINGS
# =========================================================

np.random.seed(45)

N = 90000
CUSTOMER_COUNT = 20000

print("Starting Customer ID Map Dataset...")


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

mapping_id = np.array([
    f"MAP{i:08d}"
    for i in range(1, N + 1)
])

customer_id = np.random.choice(
    customer_ids,
    N
)


# =========================================================
# SOURCE SYSTEM
# =========================================================

source_system = np.random.choice(
    [
        "CRM",
        "Website",
        "Mobile App",
        "Support",
        "Marketing",
        "Billing"
    ],
    N
)


# =========================================================
# ID TYPE
# =========================================================

id_type = np.random.choice(
    [
        "CRM_ID",
        "EMAIL_ID",
        "PHONE_ID",
        "APP_ID",
        "SUPPORT_ID",
        "MARKETING_ID"
    ],
    N
)


# =========================================================
# EXTERNAL CUSTOMER ID
# =========================================================

prefix = np.random.choice(
    [
        "CRM",
        "WEB",
        "APP",
        "SUP",
        "MKT",
        "BIL"
    ],
    N
)

random_number = np.random.randint(
    10000000,
    99999999,
    N
)

external_customer_id = np.array([
    f"{p}-{num}"
    for p, num in zip(
        prefix,
        random_number
    )
])


# =========================================================
# DATE
# =========================================================

mapping_created_date = pd.to_datetime(
    np.random.randint(
        pd.Timestamp("2023-01-01").value // 10**9,
        pd.Timestamp("2026-10-01").value // 10**9,
        N
    ),
    unit="s"
)


# =========================================================
# DATAFRAME
# =========================================================

df = pd.DataFrame({
    "mapping_id": mapping_id,
    "customer_id": customer_id,
    "source_system": source_system,
    "external_customer_id": external_customer_id,
    "id_type": id_type,
    "mapping_created_date": mapping_created_date
})


# =========================================================
# SAVE
# =========================================================

df.to_csv(
    "C:/Users/hanshika/Desktop/customer-360-intelligence/data/customer_id_map.csv",
    index=False
)


# =========================================================
# OUTPUT
# =========================================================

print("\nCustomer ID Map Dataset Created!")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nFirst 5 rows:")
print(df.head())

print("\nSource system counts:")
print(df["source_system"].value_counts())

print("\nUnique customers:")
print(df["customer_id"].nunique())

print("\nFile created:")
print("customer_id_map.csv")

print("\nDone!")