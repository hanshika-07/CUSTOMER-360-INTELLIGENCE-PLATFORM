# ============================================================
# CUSTOMER 360 INTELLIGENCE PLATFORM
# PHASE 3 - STATISTICAL ANALYSIS
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# 1. DISPLAY SETTINGS
# ============================================================

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 150)
pd.set_option("display.float_format", "{:.2f}".format)


# ============================================================
# 2. PROJECT DIRECTORIES
# ============================================================

BASE_DIR = Path(
    r"C:\Users\hanshika\Desktop\customer-360-intelligence"
)

CLEAN_DIR = BASE_DIR / "data" / "clean"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


print("=" * 70)
print("CUSTOMER 360 INTELLIGENCE PLATFORM")
print("PHASE 3 - STATISTICAL ANALYSIS")
print("=" * 70)

print("\nProject directory:")
print(BASE_DIR)

print("\nClean data directory:")
print(CLEAN_DIR)


# ============================================================
# 3. LOAD CLEANED DATA
# ============================================================

def load_csv(filename, dataset_name):

    file_path = CLEAN_DIR / filename

    if not file_path.exists():

        print("\nWARNING")
        print(f"{dataset_name} not found:")
        print(file_path)

        return None

    try:

        df = pd.read_csv(file_path)

        print(
            f"\n✓ {dataset_name} loaded"
            f" | Rows: {df.shape[0]}"
            f" | Columns: {df.shape[1]}"
        )

        return df

    except Exception as error:

        print(
            f"\nERROR loading {dataset_name}:"
            f" {error}"
        )

        return None


crm_customers = load_csv(
    "crm_customers.csv",
    "CRM Customers"
)

customer_id_map = load_csv(
    "customer_id_map.csv",
    "Customer ID Map"
)

marketing_interactions = load_csv(
    "marketing_interactions.csv",
    "Marketing Interactions"
)

orders = load_csv(
    "orders.csv",
    "Orders"
)

payments = load_csv(
    "payments.csv",
    "Payments"
)

product_usage = load_csv(
    "product_usage.csv",
    "Product Usage"
)

products = load_csv(
    "products.csv",
    "Products"
)

support_tickets = load_csv(
    "support_tickets.csv",
    "Support Tickets"
)


# ============================================================
# 4. CREATE DATASET DICTIONARY
# ============================================================

datasets = {

    "CRM Customers":
        crm_customers,

    "Customer ID Map":
        customer_id_map,

    "Marketing Interactions":
        marketing_interactions,

    "Orders":
        orders,

    "Payments":
        payments,

    "Product Usage":
        product_usage,

    "Products":
        products,

    "Support Tickets":
        support_tickets
}


# Remove missing datasets

datasets = {
    name: df
    for name, df in datasets.items()
    if df is not None
}


# ============================================================
# 5. CUSTOMER 360 DATASET OVERVIEW
# ============================================================

print("\n" + "=" * 70)
print("CUSTOMER 360 DATASET OVERVIEW")
print("=" * 70)


overview = []


for name, df in datasets.items():

    rows = df.shape[0]

    columns = df.shape[1]

    numeric_columns = len(
        df.select_dtypes(
            include=np.number
        ).columns
    )

    text_columns = len(
        df.select_dtypes(
            include="object"
        ).columns
    )

    duplicate_rows = df.duplicated().sum()

    missing_values = df.isnull().sum().sum()


    print(
        f"\n{name:<30}"
        f" Rows: {rows:>8}"
        f" | Columns: {columns:>3}"
    )


    overview.append({

        "Dataset": name,

        "Rows": rows,

        "Columns": columns,

        "Numeric Columns":
            numeric_columns,

        "Text Columns":
            text_columns,

        "Missing Values":
            missing_values,

        "Duplicate Rows":
            duplicate_rows

    })


overview_df = pd.DataFrame(overview)

print("\n")

print(overview_df.to_string(index=False))


# ============================================================
# 6. DISPLAY COLUMN NAMES
# ============================================================

print("\n" + "=" * 70)
print("COLUMN NAMES")
print("=" * 70)


for name, df in datasets.items():

    print(f"\n{name}")

    print("-" * 60)

    for column in df.columns:

        print("  ", column)


# ============================================================
# 7. DATA TYPES
# ============================================================

print("\n" + "=" * 70)
print("DATA TYPES")
print("=" * 70)


for name, df in datasets.items():

    print(f"\n{name}")

    print("-" * 60)

    print(df.dtypes)


# ============================================================
# 8. BASIC DESCRIPTIVE STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("DESCRIPTIVE STATISTICS")
print("=" * 70)


for name, df in datasets.items():

    numeric_columns = (
        df.select_dtypes(
            include=np.number
        ).columns
    )


    if len(numeric_columns) == 0:

        print(
            f"\n{name}: "
            "No numeric columns."
        )

        continue


    print(f"\n{name}")

    print("-" * 60)

    print(
        df[numeric_columns]
        .describe()
        .T
        .round(2)
    )


# ============================================================
# 9. STATISTICAL SUMMARY FUNCTION
# ============================================================

def statistical_summary(df):

    numeric_columns = (
        df.select_dtypes(
            include=np.number
        ).columns
    )

    results = []


    for column in numeric_columns:

        data = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()


        if len(data) == 0:

            continue


        mode_values = data.mode()


        mode_value = (
            mode_values.iloc[0]
            if len(mode_values) > 0
            else np.nan
        )


        results.append({

            "Column": column,

            "Mean": data.mean(),

            "Median": data.median(),

            "Mode": mode_value,

            "Minimum": data.min(),

            "Maximum": data.max(),

            "Std Dev": data.std(),

            "Variance": data.var()

        })


    return pd.DataFrame(results)


# ============================================================
# 10. STATISTICS FOR EVERY DATASET
# ============================================================

print("\n" + "=" * 70)
print("STATISTICAL SUMMARY FOR ALL DATASETS")
print("=" * 70)


all_statistics = {}


for name, df in datasets.items():

    stats = statistical_summary(df)

    all_statistics[name] = stats


    print("\n" + "=" * 70)

    print(name.upper())

    print("=" * 70)


    if stats.empty:

        print(
            "No numeric columns available."
        )

    else:

        print(
            stats.round(2)
            .to_string(index=False)
        )


# ============================================================
# 11. SAVE STATISTICAL SUMMARY
# ============================================================

statistics_output = []


for name, stats in all_statistics.items():

    if stats.empty:

        continue


    temp = stats.copy()

    temp.insert(
        0,
        "Dataset",
        name
    )

    statistics_output.append(temp)


if statistics_output:

    statistical_summary_df = pd.concat(
        statistics_output,
        ignore_index=True
    )


    statistical_summary_df.to_csv(

        REPORT_DIR /
        "statistical_summary.csv",

        index=False
    )


# ============================================================
# 12. ORDERS ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("ORDERS ANALYSIS")
print("=" * 70)


if orders is not None:

    numeric_order_columns = (
        orders
        .select_dtypes(
            include=np.number
        )
        .columns
        .tolist()
    )


    print(
        "\nNumeric columns in Orders:"
    )

    print(numeric_order_columns)


# Possible order-value column names

possible_order_columns = [

    "order_amount",

    "order_value",

    "total_amount",

    "amount",

    "revenue",

    "sales",

    "price",

    "total_price",

    "net_amount"

]


order_value_column = None


if orders is not None:

    for column in possible_order_columns:

        if column in orders.columns:

            order_value_column = column

            break


# If no known name exists, detect numeric column

if (
    order_value_column is None
    and orders is not None
):

    numeric_columns = (
        orders
        .select_dtypes(
            include=np.number
        )
        .columns
        .tolist()
    )


    # Exclude columns that look like IDs

    possible_numeric = [

        column

        for column in numeric_columns

        if "id" not in column.lower()

    ]


    if possible_numeric:

        order_value_column = (
            possible_numeric[-1]
        )


if order_value_column:

    print(
        "\nOrder value column detected:"
    )

    print(order_value_column)


    order_values = pd.to_numeric(
        orders[order_value_column],
        errors="coerce"
    ).dropna()


    if len(order_values) > 0:

        print(
            "\nAverage Order Value:",
            round(order_values.mean(), 2)
        )

        print(
            "Median Order Value:",
            round(order_values.median(), 2)
        )

        print(
            "Minimum Order Value:",
            round(order_values.min(), 2)
        )

        print(
            "Maximum Order Value:",
            round(order_values.max(), 2)
        )

        print(
            "Total Order Value:",
            round(order_values.sum(), 2)
        )

        print(
            "Order Value Std Dev:",
            round(order_values.std(), 2)
        )

else:

    print(
        "\nNo order-value column detected."
    )


# ============================================================
# 13. PAYMENT ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("PAYMENT ANALYSIS")
print("=" * 70)


payment_column = None


if payments is not None:

    print(
        "\nNumeric payment columns:"
    )

    print(
        payments
        .select_dtypes(
            include=np.number
        )
        .columns
        .tolist()
    )


possible_payment_columns = [

    "payment_amount",

    "amount",

    "paid_amount",

    "transaction_amount",

    "payment_value",

    "total_amount"

]


if payments is not None:

    for column in possible_payment_columns:

        if column in payments.columns:

            payment_column = column

            break


if (
    payment_column is None
    and payments is not None
):

    numeric_columns = (
        payments
        .select_dtypes(
            include=np.number
        )
        .columns
        .tolist()
    )


    possible_numeric = [

        column

        for column in numeric_columns

        if "id" not in column.lower()

    ]


    if possible_numeric:

        payment_column = (
            possible_numeric[-1]
        )


if payment_column:

    payment_values = pd.to_numeric(
        payments[payment_column],
        errors="coerce"
    ).dropna()


    if len(payment_values) > 0:

        print(
            "\nPayment column:",
            payment_column
        )

        print(
            "Average Payment:",
            round(payment_values.mean(), 2)
        )

        print(
            "Median Payment:",
            round(payment_values.median(), 2)
        )

        print(
            "Minimum Payment:",
            round(payment_values.min(), 2)
        )

        print(
            "Maximum Payment:",
            round(payment_values.max(), 2)
        )

        print(
            "Total Payment Value:",
            round(payment_values.sum(), 2)
        )

else:

    print(
        "\nNo payment-value column detected."
    )


# ============================================================
# 14. PRODUCT USAGE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("PRODUCT USAGE ANALYSIS")
print("=" * 70)


usage_column = None


if product_usage is not None:

    print(
        "\nNumeric usage columns:"
    )

    print(
        product_usage
        .select_dtypes(
            include=np.number
        )
        .columns
        .tolist()
    )


possible_usage_columns = [

    "usage_count",

    "usage_minutes",

    "usage_hours",

    "sessions",

    "login_count",

    "usage_value",

    "usage_frequency",

    "session_count"

]


if product_usage is not None:

    for column in possible_usage_columns:

        if column in product_usage.columns:

            usage_column = column

            break


if (
    usage_column is None
    and product_usage is not None
):

    numeric_columns = (
        product_usage
        .select_dtypes(
            include=np.number
        )
        .columns
        .tolist()
    )


    possible_numeric = [

        column

        for column in numeric_columns

        if "id" not in column.lower()

    ]


    if possible_numeric:

        usage_column = (
            possible_numeric[-1]
        )


if usage_column:

    usage_values = pd.to_numeric(
        product_usage[usage_column],
        errors="coerce"
    ).dropna()


    if len(usage_values) > 0:

        print(
            "\nUsage column:",
            usage_column
        )

        print(
            "Average Usage:",
            round(usage_values.mean(), 2)
        )

        print(
            "Median Usage:",
            round(usage_values.median(), 2)
        )

        print(
            "Minimum Usage:",
            round(usage_values.min(), 2)
        )

        print(
            "Maximum Usage:",
            round(usage_values.max(), 2)
        )

else:

    print(
        "\nNo usage-value column detected."
    )


# ============================================================
# 15. MARKETING INTERACTION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("MARKETING INTERACTION ANALYSIS")
print("=" * 70)


if marketing_interactions is not None:

    numeric_marketing_columns = (
        marketing_interactions
        .select_dtypes(
            include=np.number
        )
        .columns
        .tolist()
    )


    categorical_marketing_columns = (
        marketing_interactions
        .select_dtypes(
            exclude=np.number
        )
        .columns
        .tolist()
    )


    print(
        "\nNumeric marketing columns:"
    )

    print(
        numeric_marketing_columns
    )


    print(
        "\nCategorical marketing columns:"
    )

    print(
        categorical_marketing_columns
    )


    for column in categorical_marketing_columns:

        unique_count = (
            marketing_interactions[column]
            .nunique()
        )


        if (
            unique_count <= 20
            and unique_count > 0
        ):

            print(
                f"\n{column} distribution:"
            )

            print(
                marketing_interactions[column]
                .value_counts()
                .head(20)
            )


# ============================================================
# 16. SUPPORT TICKET ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("SUPPORT TICKET ANALYSIS")
print("=" * 70)


resolution_column = None


if support_tickets is not None:

    print(
        "\nNumeric support columns:"
    )

    print(
        support_tickets
        .select_dtypes(
            include=np.number
        )
        .columns
        .tolist()
    )


possible_resolution_columns = [

    "resolution_time",

    "resolution_hours",

    "resolution_days",

    "response_time",

    "response_hours",

    "resolution_minutes"

]


if support_tickets is not None:

    for column in possible_resolution_columns:

        if column in support_tickets.columns:

            resolution_column = column

            break


if resolution_column:

    resolution = pd.to_numeric(
        support_tickets[
            resolution_column
        ],
        errors="coerce"
    ).dropna()


    if len(resolution) > 0:

        print(
            "\nResolution column:",
            resolution_column
        )

        print(
            "Average Resolution Time:",
            round(resolution.mean(), 2)
        )

        print(
            "Median Resolution Time:",
            round(resolution.median(), 2)
        )

        print(
            "Minimum Resolution Time:",
            round(resolution.min(), 2)
        )

        print(
            "Maximum Resolution Time:",
            round(resolution.max(), 2)
        )

else:

    print(
        "\nNo resolution-time column detected."
    )


# ============================================================
# 17. CUSTOMER ID DETECTION
# ============================================================

print("\n" + "=" * 70)
print("CUSTOMER ID ANALYSIS")
print("=" * 70)


def find_customer_id_column(df):

    if df is None:

        return None


    possible_names = [

        "customer_id",

        "Customer_ID",

        "customerId",

        "cust_id",

        "customerid",

        "customer"

    ]


    for column in possible_names:

        if column in df.columns:

            return column


    # Automatic detection

    for column in df.columns:

        column_lower = column.lower()

        if (
            "customer" in column_lower
            and "id" in column_lower
        ):

            return column


    return None


customer_id_columns = {}


for name, df in datasets.items():

    column = find_customer_id_column(df)


    if column:

        customer_id_columns[name] = column


        unique_customers = (
            df[column].nunique()
        )


        print(
            f"\n{name}"
        )

        print(
            f"Customer ID Column: {column}"
        )

        print(
            f"Unique Customers : {unique_customers}"
        )


# ============================================================
# 18. CUSTOMER-LEVEL ORDER STATISTICS
# ============================================================

customer_order_stats = None


if (
    orders is not None
    and order_value_column is not None
):

    orders_customer_column = (
        find_customer_id_column(orders)
    )


    if orders_customer_column:

        print("\n" + "=" * 70)

        print(
            "CUSTOMER-LEVEL ORDER STATISTICS"
        )

        print("=" * 70)


        orders_copy = orders.copy()


        orders_copy[
            order_value_column
        ] = pd.to_numeric(
            orders_copy[
                order_value_column
            ],
            errors="coerce"
        )


        customer_order_stats = (

            orders_copy

            .groupby(
                orders_customer_column
            )

            .agg(

                total_orders=(
                    order_value_column,
                    "count"
                ),

                total_spend=(
                    order_value_column,
                    "sum"
                ),

                average_order_value=(
                    order_value_column,
                    "mean"
                ),

                maximum_order_value=(
                    order_value_column,
                    "max"
                )

            )

            .reset_index()

        )


        print(
            customer_order_stats
            .head(10)
            .to_string(index=False)
        )


# ============================================================
# 19. CUSTOMER-LEVEL PRODUCT USAGE
# ============================================================

customer_usage_stats = None


if (
    product_usage is not None
    and usage_column is not None
):

    usage_customer_column = (
        find_customer_id_column(
            product_usage
        )
    )


    if usage_customer_column:

        print("\n" + "=" * 70)

        print(
            "CUSTOMER-LEVEL PRODUCT USAGE"
        )

        print("=" * 70)


        usage_copy = (
            product_usage.copy()
        )


        usage_copy[
            usage_column
        ] = pd.to_numeric(
            usage_copy[usage_column],
            errors="coerce"
        )


        customer_usage_stats = (

            usage_copy

            .groupby(
                usage_customer_column
            )

            .agg(

                usage_records=(
                    usage_column,
                    "count"
                ),

                total_usage=(
                    usage_column,
                    "sum"
                ),

                average_usage=(
                    usage_column,
                    "mean"
                )

            )

            .reset_index()

        )


        print(
            customer_usage_stats
            .head(10)
            .to_string(index=False)
        )


# ============================================================
# 20. CUSTOMER-LEVEL SUPPORT STATISTICS
# ============================================================

customer_support_stats = None


if support_tickets is not None:

    support_customer_column = (
        find_customer_id_column(
            support_tickets
        )
    )


    if support_customer_column:

        print("\n" + "=" * 70)

        print(
            "CUSTOMER SUPPORT STATISTICS"
        )

        print("=" * 70)


        customer_support_stats = (

            support_tickets

            .groupby(
                support_customer_column
            )

            .size()

            .reset_index(
                name="support_ticket_count"
            )

        )


        print(
            customer_support_stats
            .head(10)
            .to_string(index=False)
        )


# ============================================================
# 21. CUSTOMER 360 MERGE
# ============================================================

customer_360_stats = None


if (
    customer_order_stats is not None
    and customer_usage_stats is not None
):

    order_customer_column = (
        customer_order_stats.columns[0]
    )

    usage_customer_column = (
        customer_usage_stats.columns[0]
    )


    customer_360_stats = pd.merge(

        customer_order_stats,

        customer_usage_stats,

        left_on=order_customer_column,

        right_on=usage_customer_column,

        how="outer"

    )


if (
    customer_360_stats is not None
    and customer_support_stats is not None
):

    order_customer_column = (
        customer_360_stats.columns[0]
    )

    support_customer_column = (
        customer_support_stats.columns[0]
    )


    customer_360_stats = pd.merge(

        customer_360_stats,

        customer_support_stats,

        left_on=order_customer_column,

        right_on=support_customer_column,

        how="outer"

    )


if customer_360_stats is not None:

    print("\n" + "=" * 70)

    print(
        "CUSTOMER 360 CUSTOMER-LEVEL DATASET"
    )

    print("=" * 70)


    print(
        customer_360_stats
        .head(10)
        .to_string(index=False)
    )


    customer_360_stats.to_csv(

        REPORT_DIR /
        "customer_360_customer_level_statistics.csv",

        index=False

    )


# ============================================================
# 22. IQR ANALYSIS FUNCTION
# ============================================================

def iqr_analysis(df, column):

    data = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()


    if len(data) == 0:

        return None


    q1 = data.quantile(0.25)

    median = data.quantile(0.50)

    q3 = data.quantile(0.75)

    iqr = q3 - q1


    lower_limit = (
        q1 - 1.5 * iqr
    )

    upper_limit = (
        q3 + 1.5 * iqr
    )


    outliers = data[
        (data < lower_limit)
        |
        (data > upper_limit)
    ]


    outlier_percentage = (
        len(outliers)
        /
        len(data)
        *
        100
    )


    return {

        "Column": column,

        "Q1": q1,

        "Median": median,

        "Q3": q3,

        "IQR": iqr,

        "Lower Limit": lower_limit,

        "Upper Limit": upper_limit,

        "Outliers": len(outliers),

        "Outlier %":
            outlier_percentage

    }


# ============================================================
# 23. IQR ANALYSIS - ORDERS
# ============================================================

iqr_results = []


if order_value_column:

    result = iqr_analysis(
        orders,
        order_value_column
    )


    if result:

        print("\n" + "=" * 70)

        print(
            "ORDER VALUE IQR ANALYSIS"
        )

        print("=" * 70)


        print(
            pd.DataFrame([result])
            .round(2)
            .to_string(index=False)
        )


        result["Dataset"] = "Orders"

        iqr_results.append(result)


# ============================================================
# 24. IQR ANALYSIS - PAYMENTS
# ============================================================

if payment_column:

    result = iqr_analysis(
        payments,
        payment_column
    )


    if result:

        print("\n" + "=" * 70)

        print(
            "PAYMENT VALUE IQR ANALYSIS"
        )

        print("=" * 70)


        print(
            pd.DataFrame([result])
            .round(2)
            .to_string(index=False)
        )


        result["Dataset"] = "Payments"

        iqr_results.append(result)


# ============================================================
# 25. IQR ANALYSIS - PRODUCT USAGE
# ============================================================

if usage_column:

    result = iqr_analysis(
        product_usage,
        usage_column
    )


    if result:

        print("\n" + "=" * 70)

        print(
            "PRODUCT USAGE IQR ANALYSIS"
        )

        print("=" * 70)


        print(
            pd.DataFrame([result])
            .round(2)
            .to_string(index=False)
        )


        result["Dataset"] = "Product Usage"

        iqr_results.append(result)


if iqr_results:

    iqr_df = pd.DataFrame(
        iqr_results
    )


    iqr_df.to_csv(

        REPORT_DIR /
        "iqr_outlier_analysis.csv",

        index=False

    )


# ============================================================
# 26. SKEWNESS ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("SKEWNESS ANALYSIS")
print("=" * 70)


def interpret_skewness(value):

    if value > 1:

        return "Highly right skewed"

    elif value > 0.5:

        return "Moderately right skewed"

    elif value < -1:

        return "Highly left skewed"

    elif value < -0.5:

        return "Moderately left skewed"

    else:

        return "Approximately symmetric"


skew_results = []


for name, df in datasets.items():

    numeric_columns = (
        df.select_dtypes(
            include=np.number
        ).columns
    )


    for column in numeric_columns:

        data = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()


        if len(data) > 1:

            skew_value = data.skew()


            interpretation = (
                interpret_skewness(
                    skew_value
                )
            )


            print(
                f"{name} | "
                f"{column} | "
                f"Skewness: "
                f"{skew_value:.2f} | "
                f"{interpretation}"
            )


            skew_results.append({

                "Dataset": name,

                "Column": column,

                "Skewness": skew_value,

                "Interpretation":
                    interpretation

            })


skew_df = pd.DataFrame(
    skew_results
)


if not skew_df.empty:

    skew_df.to_csv(

        REPORT_DIR /
        "skewness_analysis.csv",

        index=False

    )


# ============================================================
# 27. CORRELATION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("CORRELATION ANALYSIS")
print("=" * 70)


correlation_results = []


for name, df in datasets.items():

    numeric_columns = (
        df.select_dtypes(
            include=np.number
        ).columns
    )


    if len(numeric_columns) < 2:

        continue


    correlation_matrix = (
        df[numeric_columns]
        .corr()
    )


    print("\n" + "-" * 60)

    print(name)

    print("-" * 60)

    print(
        correlation_matrix
        .round(2)
    )


    for i in range(
        len(correlation_matrix.columns)
    ):

        for j in range(
            i + 1,
            len(correlation_matrix.columns)
        ):

            column_1 = (
                correlation_matrix
                .columns[i]
            )

            column_2 = (
                correlation_matrix
                .columns[j]
            )

            correlation_value = (
                correlation_matrix
                .iloc[i, j]
            )


            correlation_results.append({

                "Dataset": name,

                "Column 1": column_1,

                "Column 2": column_2,

                "Correlation":
                    correlation_value

            })


# Save correlations

if correlation_results:

    correlation_df = pd.DataFrame(
        correlation_results
    )


    correlation_df.to_csv(

        REPORT_DIR /
        "correlation_analysis.csv",

        index=False

    )


# ============================================================
# 28. STRONG CORRELATION RELATIONSHIPS
# ============================================================

print("\n" + "=" * 70)
print("IMPORTANT CORRELATION RELATIONSHIPS")
print("=" * 70)


strong_correlations = []


for result in correlation_results:

    value = result["Correlation"]


    if (
        not pd.isna(value)
        and abs(value) >= 0.50
    ):

        print(
            f"{result['Dataset']} | "
            f"{result['Column 1']} ↔ "
            f"{result['Column 2']} = "
            f"{value:.2f}"
        )


        strong_correlations.append(
            result
        )


if strong_correlations:

    strong_df = pd.DataFrame(
        strong_correlations
    )


    strong_df.to_csv(

        REPORT_DIR /
        "strong_correlations.csv",

        index=False

    )

else:

    print(
        "No correlation above "
        "the 0.50 threshold."
    )


# ============================================================
# 29. MISSING VALUE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("MISSING VALUE ANALYSIS")
print("=" * 70)


missing_results = []


for name, df in datasets.items():

    for column in df.columns:

        null_count = (
            df[column].isna().sum()
        )


        null_percentage = (
            df[column].isna().mean()
            * 100
        )


        if null_count > 0:

            print(
                f"{name} | "
                f"{column} | "
                f"Nulls: {null_count} | "
                f"Null %: "
                f"{null_percentage:.2f}%"
            )


        missing_results.append({

            "Dataset": name,

            "Column": column,

            "Null Count": null_count,

            "Null Percentage":
                null_percentage

        })


missing_df = pd.DataFrame(
    missing_results
)


missing_df.to_csv(

    REPORT_DIR /
    "missing_value_analysis.csv",

    index=False

)


# ============================================================
# 30. DUPLICATE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("DUPLICATE ANALYSIS")
print("=" * 70)


duplicate_results = []


for name, df in datasets.items():

    duplicate_count = (
        df.duplicated().sum()
    )


    duplicate_percentage = (

        duplicate_count
        /
        len(df)
        *
        100

        if len(df) > 0
        else 0

    )


    print(
        f"{name} | "
        f"Duplicates: "
        f"{duplicate_count} | "
        f"Duplicate %: "
        f"{duplicate_percentage:.2f}%"
    )


    duplicate_results.append({

        "Dataset": name,

        "Duplicate Rows":
            duplicate_count,

        "Duplicate Percentage":
            duplicate_percentage

    })


duplicate_df = pd.DataFrame(
    duplicate_results
)


duplicate_df.to_csv(

    REPORT_DIR /
    "duplicate_analysis.csv",

    index=False

)


# ============================================================
# 31. HISTOGRAM - ORDER VALUE
# ============================================================

if order_value_column:

    order_values = pd.to_numeric(
        orders[order_value_column],
        errors="coerce"
    ).dropna()


    if len(order_values) > 0:

        plt.figure(
            figsize=(8, 5)
        )


        plt.hist(
            order_values,
            bins=30
        )


        plt.title(
            "Distribution of Order Value"
        )

        plt.xlabel(
            "Order Value"
        )

        plt.ylabel(
            "Number of Orders"
        )


        plt.tight_layout()


        plt.savefig(

            REPORT_DIR /
            "order_value_distribution.png",

            dpi=300

        )


        plt.show()


# ============================================================
# 32. BOXPLOT - ORDER VALUE
# ============================================================

if order_value_column:

    order_values = pd.to_numeric(
        orders[order_value_column],
        errors="coerce"
    ).dropna()


    if len(order_values) > 0:

        plt.figure(
            figsize=(8, 5)
        )


        plt.boxplot(
            order_values
        )


        plt.title(
            "Order Value Outlier Analysis"
        )

        plt.ylabel(
            "Order Value"
        )


        plt.tight_layout()


        plt.savefig(

            REPORT_DIR /
            "order_value_boxplot.png",

            dpi=300

        )


        plt.show()


# ============================================================
# 33. HISTOGRAM - PAYMENT VALUE
# ============================================================

if payment_column:

    payment_values = pd.to_numeric(
        payments[payment_column],
        errors="coerce"
    ).dropna()


    if len(payment_values) > 0:

        plt.figure(
            figsize=(8, 5)
        )


        plt.hist(
            payment_values,
            bins=30
        )


        plt.title(
            "Distribution of Payment Amount"
        )

        plt.xlabel(
            "Payment Amount"
        )

        plt.ylabel(
            "Number of Payments"
        )


        plt.tight_layout()


        plt.savefig(

            REPORT_DIR /
            "payment_distribution.png",

            dpi=300

        )


        plt.show()


# ============================================================
# 34. HISTOGRAM - PRODUCT USAGE
# ============================================================

if usage_column:

    usage_values = pd.to_numeric(
        product_usage[usage_column],
        errors="coerce"
    ).dropna()


    if len(usage_values) > 0:

        plt.figure(
            figsize=(8, 5)
        )


        plt.hist(
            usage_values,
            bins=30
        )


        plt.title(
            "Distribution of Product Usage"
        )

        plt.xlabel(
            "Product Usage"
        )

        plt.ylabel(
            "Number of Records"
        )


        plt.tight_layout()


        plt.savefig(

            REPORT_DIR /
            "product_usage_distribution.png",

            dpi=300

        )


        plt.show()


# ============================================================
# 35. SAVE DATASET OVERVIEW
# ============================================================

overview_df.to_csv(

    REPORT_DIR /
    "customer_360_dataset_overview.csv",

    index=False

)


# ============================================================
# 36. FINAL MESSAGE
# ============================================================

print("\n")
print("=" * 70)
print("CUSTOMER 360 INTELLIGENCE PLATFORM")
print("PHASE 3 — STATISTICAL ANALYSIS COMPLETED")
print("=" * 70)
