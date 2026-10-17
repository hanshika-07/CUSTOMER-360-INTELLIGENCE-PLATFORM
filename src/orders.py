import numpy as np
import pandas as pd
from pathlib import Path


def generate_orders(customers, products, n=120000, seed=42):

    # Set random seed
    np.random.seed(seed)

    # ---------------------------------------------------------
    # Generate orders
    # ---------------------------------------------------------

    orders = pd.DataFrame({

        "order_id": [
            f"ORD-{i:06d}" for i in range(1, n + 1)
        ],

        "shop_cust_id": np.random.choice(
            customers["crm_id"].dropna(),
            n
        ),

        "order_date": (
            pd.to_datetime("2023-01-01")
            + pd.to_timedelta(
                np.random.randint(0, 1095, n),
                unit="D"
            )
        ),

        "product_id": np.random.choice(
            products["product_id"],
            n
        ),

        "qty": np.random.randint(
            1,
            6,
            n
        ),

        "discount_pct": np.random.choice(
            [0, 5, 10, 15, 20, 25, 30],
            n,
            p=[
                0.25,
                0.15,
                0.20,
                0.15,
                0.10,
                0.10,
                0.05
            ]
        ),

        "status": np.random.choice(
            [
                "Completed",
                "Cancelled",
                "Returned"
            ],
            n,
            p=[
                0.88,
                0.07,
                0.05
            ]
        )
    })

    # ---------------------------------------------------------
    # Get product list prices
    # ---------------------------------------------------------

    price_lookup = products.set_index(
        "product_id"
    )["list_price"]

    orders["list_price"] = (
        orders["product_id"]
        .map(price_lookup)
    )

    # ---------------------------------------------------------
    # Calculate order amount
    # ---------------------------------------------------------

    orders["amount"] = np.round(
        orders["qty"]
        * orders["list_price"]
        * (
            1 - orders["discount_pct"] / 100
        ),
        2
    )

    # ---------------------------------------------------------
    # Introduce a small number of invalid amounts
    # for data-quality analysis
    # ---------------------------------------------------------

    bad_count = int(n * 0.002)

    bad_idx = np.random.choice(
        orders.index,
        size=bad_count,
        replace=False
    )

    orders.loc[
        bad_idx,
        "amount"
    ] = np.random.choice(
        [0, -100, -250],
        size=bad_count
    )

    return orders


# =============================================================
# MAIN PROGRAM
# =============================================================

if __name__ == "__main__":

    print("Loading customers and products...")

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
    # Read previously generated datasets
    # ---------------------------------------------------------

    customers_file = (
        raw_folder
        / "C:/Users/hanshika/Desktop/customer-360-intelligence/data/crm_customers.csv"
    )

    products_file = (
        raw_folder
        / "C:/Users/hanshika/Desktop/customer-360-intelligence/data/products.csv"
    )

    customers = pd.read_csv(
        customers_file
    )

    products = pd.read_csv(
        products_file
    )

    print("Customers loaded:", len(customers))
    print("Products loaded :", len(products))

    # ---------------------------------------------------------
    # Generate orders
    # ---------------------------------------------------------

    print()
    print("Generating orders...")

    orders = generate_orders(
        customers=customers,
        products=products,
        n=120000,
        seed=42
    )

    # ---------------------------------------------------------
    # Save CSV
    # ---------------------------------------------------------

    output_file = (
        raw_folder
        / "orders.csv"
    )

    orders.to_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/orders.csv",
        index=False
    )

    # ---------------------------------------------------------
    # Display results
    # ---------------------------------------------------------

    print()
    print("Order dataset generated successfully!")
    print()

    print(f"Rows generated : {len(orders):,}")
    print(f"Columns        : {len(orders.columns)}")
    print(f"Saved to       : {output_file}")

    print()
    print("Columns:")
    print(list(orders.columns))

    print()
    print("First 5 rows:")
    print(orders.head())

    print()
    print("Order status:")
    print(orders["status"].value_counts())

    print()
    print("Discount distribution:")
    print(orders["discount_pct"].value_counts().sort_index())