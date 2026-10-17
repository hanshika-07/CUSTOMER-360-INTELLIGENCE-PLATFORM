import numpy as np
import pandas as pd
from faker import Faker
from pathlib import Path


def generate_crm_customers(n=20000, seed=42):
    
    Faker.seed(seed)
    np.random.seed(seed)

  
    fake = Faker("en_IN")

  
    cities = [
        "Jodhpur",
        "Jaipur",
        "Udaipur",
        "Delhi",
        "Mumbai",
        "Bengaluru",
        "Pune"
    ]

    channels = [
        "Referral",
        "Organic",
        "Paid Ads",
        "Email"
    ]

    plans = [
        "Basic",
        "Standard",
        "Premium"
    ]

    
    crm = pd.DataFrame({
        "crm_id": [
            f"CRM-{i:05d}" for i in range(1, n + 1)
        ],

        "full_name": [
            fake.name() for _ in range(n)
        ],

        "email": [
            fake.email() for _ in range(n)
        ],

        "phone": [
            fake.phone_number() for _ in range(n)
        ],

        "city": np.random.choice(
            cities,
            n,
            p=[
                0.10,
                0.20,
                0.10,
                0.20,
                0.20,
                0.10,
                0.10
            ]
        ),

        "channel": np.random.choice(
            channels,
            n,
            p=[
                0.20,
                0.30,
                0.30,
                0.20
            ]
        ),

        "plan": np.random.choice(
            plans,
            n,
            p=[
                0.40,
                0.40,
                0.20
            ]
        ),

        "signup_date": (
            pd.to_datetime("2023-01-01")
            + pd.to_timedelta(
                np.random.randint(0, 900, n),
                unit="D"
            )
        )
    })


    duplicate_count = int(n * 0.04)

    duplicates = crm.sample(
        duplicate_count,
        random_state=seed
    ).copy()


    duplicates["email"] = duplicates["email"] .str.upper()
    

    
    crm = pd.concat(
        [crm, duplicates],
        ignore_index=True
    )

   

    missing_count = int(len(crm) * 0.02)

    missing_idx = np.random.choice(
        crm.index,
        size=missing_count,
        replace=False
    )

    crm.loc[
        missing_idx,
        "city"
    ] = np.nan

    return crm




if __name__ == "__main__":

    print("Generating CRM customer data...")

    # Generate data
    crm = generate_crm_customers(
        n=20000,
        seed=42
    )


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

    output_file = (
        raw_folder
        / "crm_customers.csv"
    )

    crm.to_csv(
        "C:/Users/hanshika/Desktop/customer-360-intelligence/data/crm_customers.csv",
        index=False
    )

    print()
    print("CRM customer dataset generated successfully!")
    print()
    print(f"Rows generated : {len(crm):,}")
    print(f"Columns        : {len(crm.columns)}")
    print(f"Saved to       : {output_file}")
    print()

    print("Columns:")
    print(list(crm.columns))

    print()
    print("First 5 rows:")
    print(crm.head())