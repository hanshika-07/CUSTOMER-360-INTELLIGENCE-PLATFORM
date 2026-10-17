import numpy as np
import pandas as pd
from pathlib import Path


def generate_payments(orders, seed=42):

    # Set random seed
    np.random.seed(seed)

    # ---------------------------------------------------------
    # Generate payment records
    # ---------------------------------------------------------

    payments = pd.DataFrame({

        "payment_id": [
            f"PAY-{i:06d}"
            for i in range(1, len(orders) + 1)
        ],

        "order_id": orders["order_id"].values,

        "billing_cust_id": orders["shop_cust_id"].values,

        "pay_date": (
            pd.to_datetime(orders["order_date"])
            + pd.to_timedelta(
                np.random.randint(
                    0,
                    5,
                    len(orders)
                ),
                unit="D"
            )
        ),

        "method": np.random.choice(
            [
                "UPI",
                "Credit Card",
                "Debit Card",
                "Net Banking"
            ],
            len(orders),
            p=[
                0.40,
                0.25,
                0.20,
                0.15
            ]
        ),

        "status": np.random.choice(
            [
                "Paid",
                "Failed",
                "Pending"
            ],
            len(orders),
            p=[
                0.92,
                0.05,
                0.03
            ]
        )
    })

    return payments


# =============================================================
# MAIN PROGRAM
# =============================================================

if __name__ == "__main__":

    print("Loading orders...")

    # ---------------------------------------------------------
    # Find project root
    # ---------------------------------------------------------

    project_root = Path(__file__).resolve().parents[1]

    raw_folder = (
        project_root
        / "data"
        / "raw"
    )

    # ---------------------------------------------------------
    # Read orders CSV
    # ---------------------------------------------------------

    orders_file = (
        raw_folder
        / "C:/Users/hanshika/Desktop/customer-360-intelligence/data/orders.csv"
    )

    orders = pd.read_csv(
        orders_file
    )

    print(
        f"Orders loaded: {len(orders):,}"
    )

    # ---------------------------------------------------------
    # Generate payments
    # ---------------------------------------------------------

    print()
    print("Generating payment data...")

    payments = generate_payments(
        orders=orders,
        seed=42
    )

    # ---------------------------------------------------------
    # Save CSV
    # ---------------------------------------------------------

    output_file = (
        raw_folder
        / "C:/Users/hanshika/Desktop/customer-360-intelligence/data/payments.csv"
    )

    payments.to_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/payments.csv",
        index=False
    )

    # ---------------------------------------------------------
    # Display results
    # ---------------------------------------------------------

    print()
    print("Payment dataset generated successfully!")
    print()

    print(
        f"Rows generated : {len(payments):,}"
    )

    print(
        f"Columns        : {len(payments.columns)}"
    )

    print(
        f"Saved to       : {output_file}"
    )

    print()
    print("Columns:")
    print(list(payments.columns))

    print()
    print("First 5 rows:")
    print(payments.head())

    print()
    print("Payment methods:")
    print(
        payments["method"]
        .value_counts()
    )

    print()
    print("Payment status:")
    print(
        payments["status"]
        .value_counts()
    )