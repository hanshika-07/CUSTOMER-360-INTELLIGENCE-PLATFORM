import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(r"C:\Users\hanshika\Desktop\customer-360-intelligence")
CLEAN_DIR = BASE_DIR / "data" / "clean"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(exist_ok=True)

# Load datasets
customers = pd.read_csv(CLEAN_DIR / "crm_customers.csv")
orders = pd.read_csv(CLEAN_DIR / "orders.csv")
payments = pd.read_csv(CLEAN_DIR / "payments.csv")
marketing = pd.read_csv(CLEAN_DIR / "marketing_interactions.csv")

# 1. Customer distribution by city
if "city" in customers.columns:
    customers["city"].value_counts().head(10).plot(kind="bar")
    plt.title("Top 10 Cities by Customers")
    plt.xlabel("City")
    plt.ylabel("Customers")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "customers_by_city.png")
    plt.show()

# 2. Order amount distribution
amount_col = next(
    (c for c in orders.columns if c.lower() in
     ["order_amount", "amount", "total_amount", "order_value", "sales"]),
    None
)

if amount_col:
    plt.hist(orders[amount_col].dropna(), bins=20)
    plt.title("Order Amount Distribution")
    plt.xlabel("Order Amount")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "order_amount_distribution.png")
    plt.show()

# 3. Payment amount distribution
payment_col = next(
    (c for c in payments.columns if c.lower() in
     ["amount", "payment_amount", "transaction_amount"]),
    None
)

if payment_col:
    plt.boxplot(payments[payment_col].dropna())
    plt.title("Payment Amount - Outlier Analysis")
    plt.ylabel("Payment Amount")
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "payment_outliers.png")
    plt.show()

# 4. Marketing interaction types
interaction_col = next(
    (c for c in marketing.columns if c.lower() in
     ["interaction_type", "channel", "type"]),
    None
)

if interaction_col:
    marketing[interaction_col].value_counts().plot(kind="bar")
    plt.title("Marketing Interactions by Type")
    plt.xlabel("Interaction Type")
    plt.ylabel("Interactions")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "marketing_interactions.png")
    plt.show()

print("\nMatplotlib analysis completed!")
print("Charts saved in:", REPORT_DIR)