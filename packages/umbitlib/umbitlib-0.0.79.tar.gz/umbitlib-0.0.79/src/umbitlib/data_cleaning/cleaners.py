import pandas as pd
import numpy as np
from typing import List, Optional

# Text Cleaning Functions
def clean_text_columns(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Apply standardized text cleaning to specified columns.
    
    Args:
        df (pd.DataFrame): Input dataframe
        columns (list): List of columns to clean. If None, clean all object columns
    
    Returns:
        pd.DataFrame: Dataframe with cleaned text columns
    """
    if columns is None:
        columns = df.select_dtypes(include=['object']).columns.tolist()
        
    df = df.copy()
    
    for column in columns:
        if column not in df.columns:
            continue
            
        # Apply string cleaning operations
        df[column] = (df[column]
                     .astype(str)
                     .str.strip()
                     .str.lower()
                     .replace(r'\s+', ' ', regex=True)  # Replace multiple spaces
                     .replace(r'[^\w\s]', '', regex=True))  # Remove special characters
                     
    return df

def trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """Trim leading/trailing whitespace from string columns."""
    str_cols = df.select_dtypes(include='object').columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()
    return df

def replace_blank_strings_with_nan(df: pd.DataFrame) -> pd.DataFrame:
    """Replace blank or whitespace-only strings with NaN."""
    return df.replace(r'^\s*$', np.nan, regex=True)

# Column Operations
def lowercase_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to lowercase."""
    df.columns = [col.lower().strip() for col in df.columns]
    return df

def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names: lowercase, replace spaces with underscores."""
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df

def drop_specific_columns(df: pd.DataFrame, columns_to_drop: List[str]) -> pd.DataFrame:
    return df.drop(columns=columns_to_drop, errors='ignore')

def rename_specific_column(df: pd.DataFrame, old_name: str, new_name: str) -> pd.DataFrame:
    return df.rename(columns={old_name: new_name})

# Row and Column Removal
def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drop duplicate rows."""
    return df.drop_duplicates()

def drop_empty_columns(df: pd.DataFrame, threshold: float = 0.9) -> pd.DataFrame:
    """Drop columns with mostly missing values (default threshold = 90%)."""
    return df.loc[:, df.isnull().mean() < threshold]

def drop_empty_rows(df: pd.DataFrame, threshold: float = 0.9) -> pd.DataFrame:
    """Drop rows with mostly missing values (default threshold = 90%)."""
    return df.loc[df.isnull().mean(axis=1) < threshold]

def remove_constant_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove columns where all values are the same."""
    return df.loc[:, df.apply(pd.Series.nunique) > 1]

# Missing Value Handling
def fill_missing_with_value(df: pd.DataFrame, fill_value: int = 0) -> pd.DataFrame:
    """Fill missing values with a given fill value (default: 0)."""
    return df.fillna(fill_value)

def fill_missing_with_median(df: pd.DataFrame) -> pd.DataFrame:
    """Fill numeric missing values with the column median."""
    for col in df.select_dtypes(include='number').columns:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
    return df

# Date Handling
def convert_dates(df: pd.DataFrame, date_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """Convert given columns to datetime. If none given, try to infer."""
    if date_columns is None:
        date_columns = [col for col in df.columns if 'date' in col.lower()]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

# Validaters
def validate_column_presence(df, required_columns):
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    return df

def validate_data_types(df, expected_dtypes):
    for col, expected_dtype in expected_dtypes.items():
        if col in df.columns and df[col].dtype != expected_dtype:
            raise ValueError(f"Column '{col}' has incorrect dtype: expected {expected_dtype}, got {df[col].dtype}")
    return df

def validate_value_range(df, column, min_value=None, max_value=None):
    if column in df.columns:
        if min_value is not None and (df[column] < min_value).any():
            raise ValueError(f"Column '{column}' contains values below the minimum: {min_value}")
        if max_value is not None and (df[column] > max_value).any():
            raise ValueError(f"Column '{column}' contains values above the maximum: {max_value}")
    return df

def validate_no_missing_values(df, columns):
    for col in columns:
        if col in df.columns and df[col].isnull().any():
            raise ValueError(f"Column '{col}' contains missing values.")
    return df

def convert_columns_to_datetime(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Convert specified columns to datetime format.
    
    Args:
        df (pd.DataFrame): Input dataframe
        columns (List[str]): List of column names to convert to datetime
    
    Returns:
        pd.DataFrame: Dataframe with specified columns converted to datetime
    """
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors='coerce')
    return df