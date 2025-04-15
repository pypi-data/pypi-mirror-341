import pandas as pd
import sqlalchemy as sa 
# from .utils import generate_sqlalchemy_dtypes, convert_categorical_to_string, get_sqlalchemy_dtypes_by_engine
from .utils import get_sqlalchemy_dtypes_by_engine

class DatabaseInteraction:
    """
    A class to handle database interactions using SQLAlchemy and Pandas.
    Attributes:
        engine: The SQLAlchemy engine used for database connections.
    Methods:
        run_raw_sql(engine, sql_stmt):
            Executes a raw SQL statement using the provided engine.
        upload_dataframe(dataframe, name, con, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None, method=None):
            Uploads a Pandas DataFrame to a database table.
        query(sql_stmt):
            Executes a SQL query and returns the result as a Pandas DataFrame.
    """
    def __init__(self, engine):
        self.engine = engine

    def run_raw_sql(self, sql_stmt):
        """
        Executes a raw SQL statement using the database engine.

        Args:
            sql_stmt (str): The raw SQL statement to be executed.

        Returns:
            None

        Raises:
            sqlalchemy.exc.SQLAlchemyError: If there is an error during the execution of the SQL statement.

        Note:
            This method directly executes the provided SQL statement. Ensure that the input is sanitized
            to prevent SQL injection vulnerabilities.
        """
        with self.engine.begin() as connection:
            connection.execute( sa.text(sql_stmt) )            

    def upload_dataframe(self, dataframe, name, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None, method=None):        
        """
        Uploads a pandas DataFrame to a SQL database.
        Parameters:
            dataframe (pandas.DataFrame): The DataFrame to upload.
            name (str): The name of the target table in the database.
            schema (str, optional): The schema of the target table. Defaults to None.
            if_exists (str, optional): Behavior when the table already exists. 
                Options are 'fail', 'replace', or 'append'. Defaults to 'fail'.
            index (bool, optional): Whether to include the DataFrame's index as a column in the table. Defaults to True.
            index_label (str or sequence, optional): Column label(s) for the index. Defaults to None.
            chunksize (int, optional): Number of rows to write at a time. Defaults to None.
            dtype (dict or sqlalchemy.types.TypeEngine, optional): Data type for columns. If None, types are inferred. Defaults to None.
            method (str or callable, optional): The method to use for inserting data into the database. Defaults to None.
        Raises:
            ValueError: If the DataFrame is empty or invalid parameters are provided.
            sqlalchemy.exc.SQLAlchemyError: If there is an error during the database interaction.
        Notes:
            - The `dtype` parameter can be used to explicitly specify the SQL data types for the columns.
            - The `method` parameter can be used to specify a custom insertion method, such as 'multi' for batch inserts.
        Example:
            >>> db_interaction.upload_dataframe(
            ...     dataframe=df,
            ...     name='my_table',
            ...     schema='public',
            ...     if_exists='replace',
            ...     index=False
            ... )
        """
        dtypes = dtype or get_sqlalchemy_dtypes_by_engine(self.engine, dataframe)  

        with self.engine.begin() as connection:
            dataframe.to_sql(name=name, con=connection, schema=schema, if_exists=if_exists, index=index, index_label=index_label, chunksize=chunksize, dtype=dtypes, method=method) 

    def query(self, sql_stmt):
        """
        Executes a SQL query and returns the result as a pandas DataFrame.

        Args:
            sql_stmt (str): The SQL statement to execute.

        Returns:
            pandas.DataFrame: The result of the SQL query.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: If there is an error executing the query.
        """
        with self.engine.connect() as connection:
            return pd.read_sql(sa.text(sql_stmt), con=connection)