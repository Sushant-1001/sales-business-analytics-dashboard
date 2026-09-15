import pandas as pd
import numpy as np


# ============================================
# READ SALES FILE
# ============================================

def read_sales_file(file_path):
    """
    Read CSV or Excel sales file.

    Parameters:
        file_path: Path of CSV or Excel file

    Returns:
        pandas DataFrame
    """

    try:

        if file_path.lower().endswith(".csv"):
            df = pd.read_csv(file_path)

        elif file_path.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_path)

        else:
            raise ValueError("Only CSV and Excel files are supported.")

        return df

    except Exception as e:
        raise Exception(f"Error reading file: {e}")


# ============================================
# CLEAN COLUMN NAMES
# ============================================

def clean_column_names(df):
    """
    Clean column names by:
    - Removing extra spaces
    - Converting to lowercase
    - Replacing spaces with underscores
    """

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


# ============================================
# REMOVE DUPLICATES
# ============================================

def remove_duplicates(df):
    """
    Remove duplicate rows from the DataFrame.
    """

    df = df.copy()

    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    removed = before - after

    print(f"Duplicate rows removed: {removed}")

    return df


# ============================================
# HANDLE MISSING VALUES
# ============================================

def handle_missing_values(df):
    """
    Handle missing values in sales data.
    """

    df = df.copy()

    # Fill missing customer names
    if "customer_name" in df.columns:
        df["customer_name"] = (
            df["customer_name"]
            .fillna("Unknown Customer")
        )

    # Fill missing product names
    if "product_name" in df.columns:
        df["product_name"] = (
            df["product_name"]
            .fillna("Unknown Product")
        )

    # Fill missing category
    if "category" in df.columns:
        df["category"] = (
            df["category"]
            .fillna("Unknown")
        )

    # Fill missing payment method
    if "payment_method" in df.columns:
        df["payment_method"] = (
            df["payment_method"]
            .fillna("Unknown")
        )

    # Numeric columns
    numeric_columns = [
        "quantity",
        "unit_price",
        "total_amount"
    ]

    for column in numeric_columns:

        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


# ============================================
# CONVERT DATA TYPES
# ============================================

def convert_data_types(df):
    """
    Convert sales data into appropriate data types.
    """

    df = df.copy()

    # Date
    if "sale_date" in df.columns:

        df["sale_date"] = pd.to_datetime(
            df["sale_date"],
            errors="coerce"
        )

    # Quantity
    if "quantity" in df.columns:

        df["quantity"] = pd.to_numeric(
            df["quantity"],
            errors="coerce"
        )

    # Unit price
    if "unit_price" in df.columns:

        df["unit_price"] = pd.to_numeric(
            df["unit_price"],
            errors="coerce"
        )

    # Total amount
    if "total_amount" in df.columns:

        df["total_amount"] = pd.to_numeric(
            df["total_amount"],
            errors="coerce"
        )

    return df


# ============================================
# REMOVE INVALID VALUES
# ============================================

def remove_invalid_values(df):
    """
    Remove records with invalid quantity or price.
    """

    df = df.copy()

    if "quantity" in df.columns:

        df = df[
            df["quantity"].notna() &
            (df["quantity"] > 0)
        ]

    if "unit_price" in df.columns:

        df = df[
            df["unit_price"].notna() &
            (df["unit_price"] >= 0)
        ]

    return df


# ============================================
# CALCULATE TOTAL AMOUNT
# ============================================

def calculate_total_amount(df):
    """
    Calculate total amount using:

        quantity × unit_price
    """

    df = df.copy()

    if (
        "quantity" in df.columns
        and "unit_price" in df.columns
    ):

        df["total_amount"] = (
            df["quantity"] *
            df["unit_price"]
        )

    return df


# ============================================
# VALIDATE REQUIRED COLUMNS
# ============================================

def validate_sales_data(df):
    """
    Check whether required columns exist.
    """

    required_columns = [
        "sale_date",
        "customer_name",
        "product_name",
        "category",
        "quantity",
        "unit_price",
        "payment_method"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    return True


# ============================================
# COMPLETE DATA CLEANING PIPELINE
# ============================================

def clean_sales_data(file_path):
    """
    Complete sales data cleaning pipeline.

    Steps:
        1. Read file
        2. Clean column names
        3. Validate columns
        4. Remove duplicates
        5. Handle missing values
        6. Convert data types
        7. Remove invalid values
        8. Calculate total amount

    Returns:
        Cleaned DataFrame
    """

    # Step 1
    df = read_sales_file(file_path)

    # Step 2
    df = clean_column_names(df)

    # Step 3
    validate_sales_data(df)

    # Step 4
    df = remove_duplicates(df)

    # Step 5
    df = handle_missing_values(df)

    # Step 6
    df = convert_data_types(df)

    # Step 7
    df = remove_invalid_values(df)

    # Step 8
    df = calculate_total_amount(df)

    # Reset index
    df = df.reset_index(drop=True)

    return df