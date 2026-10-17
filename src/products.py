import numpy as np
import pandas as pd
from pathlib import Path


def generate_products(n=200, seed=42):

    # Set random seed
    np.random.seed(seed)

    # Product categories
    categories = [
        "Electronics",
        "Grocery",
        "Clothing",
        "Home",
        "Beauty",
        "Sports",
        "Accessories",
        "Books"
    ]

    # Generate products
    products = pd.DataFrame({

        "product_id": [
            f"P-{i:04d}" for i in range(1, n + 1)
        ],

        "product_name": [
            f"Product {i:04d}" for i in range(1, n + 1)
        ],

        "category": np.random.choice(
            categories,
            n
        ),

        "unit_cost": np.round(
            np.random.uniform(100, 5000, n),
            2
        )
    })

    # Generate selling price
    products["list_price"] = np.round(
        products["unit_cost"]
        * np.random.uniform(1.2, 2.5, n),
        2
    )

    return products


# =============================================================
# MAIN PROGRAM
# =============================================================

if __name__ == "__main__":

    print("Generating product data...")

    # Generate products
    products = generate_products(
        n=200,
        seed=42
    )

    # ---------------------------------------------------------
    # Create data/raw folder
    # ---------------------------------------------------------

    project_root = Path(__file__).resolve().parents[1]

    raw_folder = (
        project_root
        / "data"
        / "raw"
    )

    raw_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    # ---------------------------------------------------------
    # Save CSV
    # ---------------------------------------------------------

    output_file = (
        raw_folder
        / "products.csv"
    )

    products.to_csv("C:/Users/hanshika/Desktop/customer-360-intelligence/data/products.csv",
        index=False
    )

    # ---------------------------------------------------------
    # Display results
    # ---------------------------------------------------------

    print()
    print("Product dataset generated successfully!")
    print()

    print(f"Rows generated : {len(products):,}")
    print(f"Columns        : {len(products.columns)}")
    print(f"Saved to       : {output_file}")

    print()
    print("Columns:")
    print(list(products.columns))

    print()
    print("First 5 rows:")
    print(products.head())