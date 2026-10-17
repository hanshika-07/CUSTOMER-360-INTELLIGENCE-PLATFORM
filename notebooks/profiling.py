import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# 1. PATH
# ============================================================

BASE = Path(r"C:\Users\hanshika\Desktop\customer-360-intelligence")
DATA = BASE / "data" / "clean"
REPORTS = BASE / "reports"

REPORTS.mkdir(exist_ok=True)

# ============================================================
# 2. LOAD DATA
# ============================================================

customers = pd.read_csv(DATA / "crm_customers.csv")
orders = pd.read_csv(DATA / "orders.csv")
payments = pd.read_csv(DATA / "payments.csv")
usage = pd.read_csv(DATA / "product_usage.csv")
marketing = pd.read_csv(DATA / "marketing_interactions.csv")

# ============================================================
# 3. DATE ANALYSIS
# ============================================================

customers["signup_date"] = pd.to_datetime(
customers["signup_date"], errors="coerce"
)


orders["order_date"] = pd.to_datetime(
    orders["order_date"], errors="coerce"
)

# ============================================================
# 4. ORDER METRICS
# ============================================================

order_stats = orders.groupby("shop_cust_id").agg(
    total_transactions=("order_id", "count"),
    total_spend=("amount", "sum"),
    average_transaction_value=("amount", "mean")
).reset_index().rename(columns={"shop_cust_id": "crm_id"})

order_stats["purchase_frequency"] = order_stats["total_transactions"]

# 5. PAYMENT METRICS
payment_stats = payments.groupby("billing_cust_id").agg(
    total_payments=("payment_id", "count")
).reset_index().rename(columns={"billing_cust_id": "crm_id"})

# ============================================================
# 6. PRODUCT USAGE
# ============================================================

usage_stats = usage.groupby("customer_id").size().reset_index(
    name="usage_count"
)

usage_stats["engagement_rate"] = np.where(
    usage_stats["usage_count"] > 0,
    usage_stats["usage_count"] /
    usage_stats["usage_count"].max() * 100,
    0
)

# ============================================================
# 7. MARKETING INTERACTIONS
# ============================================================

marketing_stats = marketing.groupby("customer_id").size().reset_index(
    name="marketing_interactions"
)

# ============================================================
# 8. MERGE DATASETS
# ============================================================

customer_360 = customers.merge(
    order_stats, on="crm_id", how="left"
)

customer_360 = customer_360.merge(
    payment_stats, on="crm_id", how="left"
)

customer_360 = customer_360.merge(
    usage_stats, on="crm_id", how="left"
)

customer_360 = customer_360.merge(
    marketing_stats, on="crm_id", how="left"
)

# ============================================================
# 9. FILL MISSING VALUES
# ============================================================

numeric_cols = customer_360.select_dtypes(
    include=np.number
).columns

customer_360[numeric_cols] = (
    customer_360[numeric_cols].fillna(0)
)

# ============================================================
# 10. CLV
# ============================================================

customer_360["customer_lifetime_value"] = (
    customer_360["average_transaction_value"] *
    customer_360["purchase_frequency"]
)

# ============================================================
# 11. CUSTOMER SEGMENT USING NUMPY
# ============================================================

customer_360["value_segment"] = np.select(
    [
        customer_360["customer_lifetime_value"] >=
        customer_360["customer_lifetime_value"].quantile(0.75),

        customer_360["customer_lifetime_value"] >=
        customer_360["customer_lifetime_value"].quantile(0.50)
    ],
    [
        "High Value",
        "Medium Value"
    ],
    default="Low Value"
)

# ============================================================
# 12. PIVOT TABLE
# ============================================================

pivot = pd.pivot_table(
    orders,
    values="amount",
    index="customer_id",
    columns="transaction_type",
    aggfunc="sum",
    fill_value=0
)

pivot.to_csv(
    REPORTS / "customer_transaction_pivot.csv"
)

# ============================================================
# 13. MONTHLY TRANSACTION ANALYSIS
# ============================================================

monthly_transactions = (
    orders
    .set_index("transaction_date")
    .resample("ME")["amount"]
    .agg(["sum", "mean", "count"])
    .reset_index()
)

monthly_transactions.to_csv(
    REPORTS / "monthly_transaction_analysis.csv",
    index=False
)

# ============================================================
# 14. FILTER HIGH-VALUE CUSTOMERS
# ============================================================

high_value = customer_360[
    customer_360["value_segment"] == "High Value"
]

high_value.to_csv(
    REPORTS / "high_value_customers.csv",
    index=False
)

# ============================================================
# 15. SAVE FINAL ANALYTICAL DATASET
# ============================================================

output = REPORTS / "customer_360_analytical_dataset.csv"

customer_360.to_csv(
    output,
    index=False
)

print("=" * 60)
print("PHASE 4 COMPLETED")
print("=" * 60)
print("Rows:", len(customer_360))
print("Columns:", len(customer_360.columns))
print("Saved:", output)
