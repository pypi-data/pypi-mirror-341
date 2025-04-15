import pandas as pd
import sqlalchemy as sa
from datetime import datetime
import numpy as np

def create_mock_dataframe():
    """
    Creates a mock pandas DataFrame with various data types for testing
    the generate_sqlalchemy_dtypes function.
    """
    data = {
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 28, 35, 22],
        'height': [165.5, 178.2, 170.0, 182.8, 158.7],
        'is_student': [True, False, False, True, False],
        'enrollment_date': [
            datetime(2023, 9, 1),
            datetime(2022, 11, 15),
            datetime(2024, 3, 10),
            datetime(2023, 5, 20),
            datetime(2024, 1, 5),
        ],
        'score': [85, 92, 78, 95, 88],
        'notes': ['Good', None, 'Average', 'Excellent', 'Good'],
        'weight': [60.2, 75.8, 70.5, np.nan, 55.9],
        'category': pd.Categorical(['A', 'B', 'A', 'C', 'B']),
    }
    df = pd.DataFrame(data)
    return df

def generate_sqlalchemy_dtypes_oracle(dataframe):
    """
    Generate SQLAlchemy column types for Oracle based on DataFrame dtypes.
    """
    sqlalchemy_dtypes = {}
    for col_name, col_dtype in dataframe.dtypes.items():
        if pd.api.types.is_integer_dtype(col_dtype):
            sqlalchemy_dtypes[col_name] = sa.types.NUMERIC(precision=38, scale=0)  # Oracle's equivalent of BigInteger
        elif pd.api.types.is_float_dtype(col_dtype):
            sqlalchemy_dtypes[col_name] = sa.types.FLOAT()
        elif pd.api.types.is_bool_dtype(col_dtype):
            sqlalchemy_dtypes[col_name] = sa.types.NUMERIC(precision=1)  # Store as 0 or 1
        elif pd.api.types.is_string_dtype(col_dtype):
            max_length = dataframe[col_name].astype(str).apply(len).max()
            sqlalchemy_dtypes[col_name] = sa.types.VARCHAR(length=max_length)
        elif pd.api.types.is_datetime64_any_dtype(col_dtype):
            sqlalchemy_dtypes[col_name] = sa.types.TIMESTAMP()
        elif pd.api.types.is_categorical_dtype(col_dtype):
            max_length = dataframe[col_name].astype(str).apply(len).max()
            sqlalchemy_dtypes[col_name] = sa.types.VARCHAR(length=max_length)
        elif col_dtype == 'object':
            max_length = dataframe[col_name].astype(str).apply(len).max()
            sqlalchemy_dtypes[col_name] = sa.types.VARCHAR(length=max_length)
        else:
            max_length = dataframe[col_name].astype(str).apply(len).max()
            sqlalchemy_dtypes[col_name] = sa.types.VARCHAR(length=max_length)
    return sqlalchemy_dtypes

def generate_sqlalchemy_dtypes_postgresql(dataframe):
    """
    Generate SQLAlchemy column types for PostgreSQL based on DataFrame dtypes
    using VARCHAR with maximum length.
    """
    sqlalchemy_dtypes = {}
    for col_name, col_dtype in dataframe.dtypes.items():
        if pd.api.types.is_integer_dtype(col_dtype):
            sqlalchemy_dtypes[col_name] = sa.types.INTEGER()
        elif pd.api.types.is_float_dtype(col_dtype):
            sqlalchemy_dtypes[col_name] = sa.types.FLOAT()
        elif pd.api.types.is_bool_dtype(col_dtype):
            sqlalchemy_dtypes[col_name] = sa.types.BOOLEAN()
        elif pd.api.types.is_string_dtype(col_dtype):
            max_length = dataframe[col_name].astype(str).apply(len).max()
            sqlalchemy_dtypes[col_name] = sa.types.VARCHAR(length=max_length)
        elif pd.api.types.is_datetime64_any_dtype(col_dtype):
            sqlalchemy_dtypes[col_name] = sa.types.TIMESTAMP()
        elif pd.api.types.is_categorical_dtype(col_dtype):
            max_length = dataframe[col_name].astype(str).apply(len).max()
            sqlalchemy_dtypes[col_name] = sa.types.VARCHAR(length=max_length)
        elif col_dtype == 'object':
            max_length = dataframe[col_name].astype(str).apply(len).max()
            sqlalchemy_dtypes[col_name] = sa.types.VARCHAR(length=max_length)
        else:
            max_length = dataframe[col_name].astype(str).apply(len).max()
            sqlalchemy_dtypes[col_name] = sa.types.VARCHAR(length=max_length)
    return sqlalchemy_dtypes

def get_sqlalchemy_dtypes_by_engine(engine: sa.Engine, dataframe: pd.DataFrame) -> dict:
    """
    Detects the database type from the SQLAlchemy engine and returns the
    appropriate dictionary of SQLAlchemy column types for the DataFrame.

    Args:
        engine: The SQLAlchemy engine object.
        dataframe: The pandas DataFrame.

    Returns:
        dict: A dictionary mapping column names to SQLAlchemy column types.
              Returns None if the database type is not recognized.
    """
    dialect_name = engine.dialect.name
    if dialect_name == 'oracle':
        return generate_sqlalchemy_dtypes_oracle(dataframe)
    elif dialect_name == 'postgresql':
        return generate_sqlalchemy_dtypes_postgresql(dataframe)
    else:
        print(f"Warning: Unsupported database dialect '{dialect_name}'. Returning None for dtype mapping.")
        return None
