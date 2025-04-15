# Database

## Overview
Contains multiple files, classes, and functions used to carry out the following tasks:
- Retrieve credentials securely using Keyring.
- Retrieve, verify structure, and load database configuration for the purpose of creating a database engine
- Create database connection engine dependent on database type
- Execute sql commands against those databases

The main file to be used is the sql_handler.py

# SQL_handler.py
This Python module provides a `SqlHandler` class, a convenience class that orchestrates database connections and interactions by integrating various utility classes.

## Class: SqlHandler

### Description

The `SqlHandler` class acts as a high-level interface for managing SQL database connections and operations. It simplifies the process of connecting to databases by handling credential retrieval, configuration loading, engine creation, and database interactions. This class brings together the functionalities of `CredentialProvider`, `DatabaseConfigLoader`, `DatabaseEngineCreator`, and `DatabaseInteraction` to provide a unified database access layer.

### Attributes

* `service_name` (str): The name of the database service. Should be the keyring service name assigned to that credential.  This should also be used as the main key in the config file in order to access that service_name's config.
* `username` (str, optional): The username for authentication. Defaults to `None`.
* `_credentials` (dict): The credentials retrieved from the system's keyring using `CredentialProvider`.
* `engine` (sqlalchemy.engine.Engine): The SQLAlchemy engine used for database connections, created by `DatabaseEngineCreator`.
* `db_interaction` (DatabaseInteraction): An object for interacting with the database, handling query execution and DataFrame uploads.

### Methods

#### `__init__(service_name: str, username: str = None, custom_config_path: str = None)`

* **Description**: Initializes the `SqlHandler` object.
* **Parameters**:
    * `service_name` (str): The name of the database service.
    * `username` (str, optional): The username for authentication. Defaults to `None`.
    * `custom_config_path` (str, optional): The path to a custom database configuration file. If provided, the connection is established using this configuration; otherwise, the default configuration is used.
* **Functionality**:
    * Retrieves database credentials from the keyring using `CredentialProvider`.
    * Establishes a database connection using either the default or a custom configuration file, based on the `custom_config_path` parameter.
    * Initializes a `DatabaseInteraction` object with the created database engine.

#### `connect_from_config() -> sqlalchemy.engine.Engine`

* **Description**: Establishes a database connection using the default configuration file (`DB_CONFIG_PATH`).
* **Functionality**:
    * Loads the database configuration from the default configuration file using `DatabaseConfigLoader`.
    * Creates a SQLAlchemy engine using `DatabaseEngineCreator` with the retrieved credentials and configuration.
    * Returns the created SQLAlchemy engine.
* **Returns**:
    * `sqlalchemy.engine.Engine`: The created SQLAlchemy engine.

#### `connect_from_custom_config(config_path: str) -> sqlalchemy.engine.Engine`

* **Description**: Establishes a database connection using a custom configuration file.
* **Parameters**:
    * `config_path` (str): The path to the custom database configuration file.
* **Functionality**:
    * Loads the database configuration from the specified `config_path` using `DatabaseConfigLoader`.
    * Creates a SQLAlchemy engine using `DatabaseEngineCreator` with the retrieved credentials and configuration.
    * Returns the created SQLAlchemy engine.
* **Returns**:
    * `sqlalchemy.engine.Engine`: The created SQLAlchemy engine.

## Usage

1.  **Installation**:
    Ensure the necessary libraries and modules are available:

    ```bash
    pip install sqlalchemy psycopg2 cx_Oracle keyring pandas
    ```

    Also, ensure that the other modules (`credential_provider`, `config_loader`, `engine_creator`, `db_interactions`) are in the same directory or accessible via your python path.

2.  **Example**:

    ```python
    from your_module.sql_handler import SqlHandler #replace your_module
    import pandas as pd

    # Example usage with default configuration
    sql_handler = SqlHandler(service_name="postgres_db", username="myuser")

    # Example usage with a custom config
    #sql_handler = SqlHandler(service_name="oracle_db", username="myuser", custom_config_path="path/to/my_config.json")

    # Example query execution
    query = "SELECT * FROM my_table LIMIT 10"
    result_df = sql_handler.db_interaction.query(query)
    print(result_df)

    #Example DataFrame Upload.
    df = pd.DataFrame({'a':[1,2,3], 'b':['x','y','z']})
    sql_handler.db_interaction.upload_dataframe(df, 'test_table', if_exists='replace')

    #Example raw sql execution.
    sql_handler.db_interaction.run_raw_sql("DELETE FROM test_table WHERE a = 1")

    #query to show the delete.
    result_df = sql_handler.db_interaction.query("SELECT * FROM test_table")
    print(result_df)
    ```

    This example demonstrates how to create an `SqlHandler` object, execute a query, upload a dataframe, and execute raw sql. The `SqlHandler` class simplifies database operations by managing the underlying complexities of credential retrieval, configuration loading, and engine creation. Note the change to the `upload_dataframe` and `run_raw_sql` calls. They now no longer require the engine as an argument.

# Other Files (Listed in alphabetical order)
Below are all the files, classes and functions that are used by sql_handler.py. Due to the modular nature of the database files, each of these can be used a standalone.  For example if you create your own database engine you could still use the db_interaction.py file and pass those methods your custom engine.

# Config_loader.py

This Python module provides a `DatabaseConfigLoader` class that loads and validates database configuration from a JSON file.

## Class: DatabaseConfigLoader

### Description

The `DatabaseConfigLoader` class is designed to load and validate database configuration settings from a JSON file. It ensures that the configuration adheres to the required structure and contains all necessary keys.

### Methods

#### `validate_database_config(config: dict) -> None`

* **Description**: Validates the provided database configuration dictionary.
* **Parameters**:
    * `config` (dict): A dictionary containing database configuration settings. The dictionary should have database names as keys, and each database's configuration as a nested dictionary.
* **Functionality**:
    * Iterates through the provided `config` dictionary.
    * Checks if each database's configuration is a dictionary.
    * Ensures that each database configuration contains the required keys: `"type"`, `"host"`, `"port"`, and `"database"`.
    * Validates the `"type"` key to be either `"postgres"` or `"oracle"`.
    * Validates that the `"port"` key is an integer.
* **Raises**:
    * `ValueError`: If the configuration is invalid, such as missing keys, incorrect data types, or unsupported database types.

#### `load_database_config(config_file: str) -> dict`

* **Description**: Loads and validates database configuration from a JSON file.
* **Parameters**:
    * `config_file` (str): The path to the JSON configuration file.
* **Functionality**:
    * Opens and reads the JSON file specified by `config_file`.
    * Parses the JSON content and extracts the `"databases"` section.
    * Calls the `validate_database_config` method to validate the loaded configuration.
    * Returns the validated database configuration dictionary.
* **Returns**:
    * `dict`: A dictionary containing the loaded and validated database configuration.
* **Raises**:
    * `FileNotFoundError`: If the specified configuration file does not exist.
    * `json.JSONDecodeError`: If the configuration file is not valid JSON.
    * `ValueError`: If the configuration within the JSON file is invalid.

## Usage

1.  **Installation**:
    No installation is required as this is a single class and utilizes Python's standard libraries.

2.  **Example**:

    **JSON Configuration File (config.json):**

    ```json
    {
      "databases": {
        "db1": {
          "type": "postgres",
          "host": "localhost",
          "port": 5432,
          "database": "mydatabase"
        },
        "db2": {
          "type": "oracle",
          "host": "192.168.1.100",
          "port": 1521,
          "database": "oracledb"
        }
      }
    }
    ```

    **Python Code:**

    ```python
    import json

    class DatabaseConfigLoader:
        # ... (class definition as provided) ...

    loader = DatabaseConfigLoader()
    try:
        config = loader.load_database_config("config.json")
        print(config)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Error loading configuration: {e}")

    ```

    This example demonstrates how to create an instance of `DatabaseConfigLoader`, load the configuration from a JSON file, and handle potential errors during the loading and validation process. The output will be the dictionary representation of the database configurations.

# Credential_provider.py
Stores class and methods for getting credentials from various sources

## Class: CredentialProvider

### Description

The `CredentialProvider` class is designed to retrieve credentials (username and password) from the system's keyring. It uses the `keyring` library to access stored credentials.

### Methods

#### `get_keyring_credentials(service_name: str, username: Optional[str] = None, encode_password: bool = True) -> Optional[Dict[str, str]]`

* **Description**: Retrieves credentials from the system's keyring.
* **Parameters**:
    * `service_name` (str): The name of the service for which credentials are stored in the keyring.
    * `username` (Optional[str], default=None): The username associated with the credentials. If `None`, the keyring will attempt to retrieve credentials without a specific username.
    * `encode_password` (bool, default=True): If `True`, the retrieved password will be URL-encoded using `urllib.parse.quote_plus`. If `False`, the password will be returned as is.
* **Functionality**:
    * Uses the `keyring.get_credential` function to retrieve credentials based on the provided `service_name` and `username`.
    * If credentials are found, it constructs a dictionary containing the `"username"` and `"password"`.
    * If `encode_password` is `True`, it URL-encodes the password before adding it to the dictionary.
    * If no credentials are found, it returns `None`.
    * Handles potential exceptions during credential retrieval and prints an error message.
* **Returns**:
    * `Optional[Dict[str, str]]`: A dictionary containing the `"username"` and `"password"` if credentials are found, or `None` if no credentials are found or an error occurs.
* **Error Handling:**
    * If an exception occurs during the credential retrieval, it prints an error message to standard output, and returns None.

## Usage

1.  **Installation**:
    Ensure the `keyring` library is installed:

    ```bash
    pip install keyring
    ```

2.  **Example**:

    ```python
    import keyring
    from typing import Optional, Dict
    from urllib.parse import quote_plus

    class CredentialProvider:
        """Retrieves credentials from various sources."""

        def get_keyring_credentials(self, service_name: str, username: Optional[str] = None, encode_password: bool = True) -> Optional[Dict[str, str]]:
            """Retrieves credentials from the system's keyring."""
            try:
                credential_obj = keyring.get_credential(service_name, username)
                if credential_obj:
                    password = quote_plus(credential_obj.password) if encode_password else credential_obj.password
                    return {"username": credential_obj.username, "password": password}
                else:
                    return None
            except Exception as e:
                print(f"Error retrieving credentials for service '{service_name}' and username '{username}': {e}")
                return None

    # Example usage:
    provider = CredentialProvider()
    credentials = provider.get_keyring_credentials("my_service", "my_user")

    if credentials:
        print(f"Username: {credentials['username']}")
        print(f"Password: {credentials['password']}")
    else:
        print("Credentials not found or an error occurred.")

    # example without encoding
    credentials = provider.get_keyring_credentials("my_service", "my_user", encode_password=False)
    if credentials:
        print(f"Username: {credentials['username']}")
        print(f"Password: {credentials['password']}")
    else:
        print("Credentials not found or an error occurred.")

    ```

    This example demonstrates how to create an instance of `CredentialProvider` and retrieve credentials for a specific service and username. It also shows how to toggle the password encoding. It handles the case where credentials are not found or an error occurs during retrieval.


# Db_interaction.py

This Python module provides a `DatabaseInteraction` class that simplifies database interactions using SQLAlchemy and Pandas.

## Class: DatabaseInteraction

### Description

The `DatabaseInteraction` class facilitates database operations by encapsulating SQLAlchemy engine management and Pandas DataFrame integration. It provides methods for executing raw SQL queries, uploading DataFrames to database tables, and retrieving query results as DataFrames.

### Attributes

* `engine`: The SQLAlchemy engine used for database connections. This engine is initialized when the `DatabaseInteraction` object is created.

### Methods

#### `__init__(engine)`

* **Description**: Initializes the `DatabaseInteraction` object with a SQLAlchemy engine.
* **Parameters**:
    * `engine` (sqlalchemy.engine.Engine): The SQLAlchemy engine to be used for database connections.

#### `run_raw_sql(sql_stmt)`

* **Description**: Executes a raw SQL statement using the database engine.
* **Parameters**:
    * `sql_stmt` (str): The SQL statement to execute.
* **Functionality**:
    * Opens a transaction using `self.engine.begin()`.
    * Executes the provided SQL statement using `connection.execute(sa.text(sql_stmt))`.
    * The transaction is automatically committed or rolled back based on the execution result.
* **Returns**:
    * `None`
* **Raises**:
    * `sqlalchemy.exc.SQLAlchemyError`: If there is an error during the execution of the SQL statement.
* **Note**:
    * This method directly executes the provided SQL statement. Ensure that the input is sanitized to prevent SQL injection vulnerabilities.

#### `upload_dataframe(dataframe, name, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None, method=None)`

* **Description**: Uploads a Pandas DataFrame to a database table.
* **Parameters**:
    * `dataframe` (pandas.DataFrame): The DataFrame to upload.
    * `name` (str): The name of the database table.
    * `schema` (str, optional): The database schema (if applicable).
    * `if_exists` (str, default='fail'): How to handle existing tables ('fail', 'replace', 'append').
    * `index` (bool, default=True): Write DataFrame index as a column.
    * `index_label` (str or sequence, optional): Column label(s) for index column(s).
    * `chunksize` (int, optional): Number of rows to write at a time.
    * `dtype` (dict, optional): Specifies the data types of columns. If not provided, it will use the `generate_sqlalchemy_dtypes` function.
    * `method` (str, optional): Specifies the SQLAlchemy method to use.
* **Functionality**:
    * Determines the data types of the DataFrame columns using the provided `dtype` or the `generate_sqlalchemy_dtypes` function.
    * Opens a transaction using `self.engine.begin()`.
    * Uses the `dataframe.to_sql()` method to upload the DataFrame to the database table.
    * The transaction is automatically committed or rolled back.
* **Returns**:
    * `None`
* **Raises**:
    * `ValueError`: If the DataFrame is empty or invalid parameters are provided.
    * `sqlalchemy.exc.SQLAlchemyError`: If there is an error during the database interaction.
* **Notes**:
    * The `dtype` parameter can be used to explicitly specify the SQL data types for the columns.
    * The `method` parameter can be used to specify a custom insertion method, such as 'multi' for batch inserts.
* **Example**:
    ```python
    db_interaction.upload_dataframe(
        dataframe=df,
        name='my_table',
        schema='public',
        if_exists='replace',
        index=False
    )
    ```

#### `query(sql_stmt)`

* **Description**: Executes a SQL query and returns the result as a Pandas DataFrame.
* **Parameters**:
    * `sql_stmt` (str): The SQL query to execute.
* **Functionality**:
    * Opens a connection using `self.engine.connect()`.
    * Uses `pd.read_sql()` to execute the SQL query and read the results into a DataFrame.
* **Returns**:
    * `pandas.DataFrame`: The result of the SQL query as a DataFrame.
* **Raises**:
    * `sqlalchemy.exc.SQLAlchemyError`: If there is an error executing the query.

## Usage

1.  **Installation**:
    Ensure the `pandas` and `sqlalchemy` libraries are installed:

    ```bash
    pip install pandas sqlalchemy
    ```

2.  **Example**:

    ```python
    import pandas as pd
    import sqlalchemy as sa
    from your_module.utils import generate_sqlalchemy_dtypes # Replace your_module

    class DatabaseInteraction:
        # ... (class definition as provided) ...

    # Example database connection string
    db_connection_string = "sqlite:///:memory:" # Example for an in memory sqlite db

    # Create a SQLAlchemy engine
    engine = sa.create_engine(db_connection_string)

    # Create a DatabaseInteraction object
    db_interaction = DatabaseInteraction(engine)

    # Example DataFrame
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})

    # Upload DataFrame to database
    db_interaction.upload_dataframe(df, "my_table", if_exists="replace")

    # Execute a query
    result_df = db_interaction.query("SELECT * FROM my_table")

    # Print the result
    print(result_df)

    # Execute raw sql
    db_interaction.run_raw_sql("DELETE FROM my_table WHERE col1 = 1")

    # query again to show the delete.
    result_df = db_interaction.query("SELECT * FROM my_table")
    print(result_df)
    ```

    This example demonstrates how to create a `DatabaseInteraction` object, upload a DataFrame to a database table, execute a SQL query, and execute raw sql. Remember to replace `"your_module.utils"` with the actual path to your `generate_sqlalchemy_dtypes` function.

# Engine_creator.py

This Python module provides a `DatabaseEngineCreator` class that creates SQLAlchemy database engines from configuration and credentials.

## Class: DatabaseEngineCreator

### Description

The `DatabaseEngineCreator` class is responsible for creating SQLAlchemy engine objects based on provided database configuration and credentials. It utilizes engine factories for different database types (PostgreSQL and Oracle).

### Methods

#### `create_engine_from_config(db_name: str, credentials: Dict[str, str], config: Dict[str, Dict]) -> Optional[sa.Engine]`

* **Description**: Creates a database engine from the provided configuration.
* **Parameters**:
    * `db_name` (str): The name of the database for which to create the engine.
    * `credentials` (Dict[str, str]): A dictionary containing database credentials (username and password).
    * `config` (Dict[str, Dict]): A dictionary containing database configurations, where keys are database names and values are configuration dictionaries.
* **Functionality**:
    * Retrieves the configuration for the specified `db_name` from the `config` dictionary.
    * If the database configuration is not found, it prints an error message and returns `None`.
    * Determines the database type from the configuration.
    * Based on the database type, it creates an appropriate engine factory (`PostgresEngineFactory` or `OracleEngineFactory`).
    * Uses the factory to create a SQLAlchemy engine using the provided credentials and database configuration details (host, port, database/service_name).
    * If the database type is not supported, it prints an error message and returns `None`.
* **Returns**:
    * `Optional[sa.Engine]`: A SQLAlchemy engine object if creation is successful, or `None` if an error occurs or the database type is unsupported.

## Usage

1.  **Installation**:
    Ensure the `sqlalchemy` library and any necessary database drivers (e.g., `psycopg2` for PostgreSQL, `cx_Oracle` for Oracle) are installed:

    ```bash
    pip install sqlalchemy psycopg2 cx_Oracle
    ```

2.  **Example**:

    ```python
    import sqlalchemy as sa
    from typing import Dict, Optional
    from your_module.engine_factories import PostgresEngineFactory, OracleEngineFactory #Replace your_module

    class DatabaseEngineCreator:
        """Creates database engines from configuration and credentials."""

        def create_engine_from_config(self, db_name: str, credentials: Dict[str, str], config: Dict[str, Dict]) -> Optional[sa.Engine]:
            """Creates a database engine from the configuration."""
            db_config = config.get(db_name)
            if not db_config:
                print(f"Database '{db_name}' not found in configuration.")
                return None

            db_type = db_config.get("type")
            if db_type == "postgres":
                factory = PostgresEngineFactory()
                return factory.create_engine(credentials, db_config["host"], db_config["port"], db_config["database"])
            elif db_type == "oracle":
                factory = OracleEngineFactory()
                return factory.create_engine(credentials, db_config["host"], db_config["port"], db_config["database"]) #database is the oracle service_name.
            else:
                print(f"Unsupported database type: {db_type}")
                return None

    # Example configuration and credentials
    config = {
        "postgres_db": {
            "type": "postgres",
            "host": "localhost",
            "port": 5432,
            "database": "mydatabase"
        },
        "oracle_db": {
            "type": "oracle",
            "host": "192.168.1.100",
            "port": 1521,
            "database": "oracleservice"
        }
    }

    credentials = {
        "username": "myuser",
        "password": "mypassword"
    }

    # Create a DatabaseEngineCreator object
    engine_creator = DatabaseEngineCreator()

    # Create a PostgreSQL engine
    postgres_engine = engine_creator.create_engine_from_config("postgres_db", credentials, config)

    # Create an Oracle engine
    oracle_engine = engine_creator.create_engine_from_config("oracle_db", credentials, config)

    if postgres_engine:
        print("PostgreSQL engine created successfully.")
        # Use postgres_engine...
    else:
        print("Failed to create PostgreSQL engine.")

    if oracle_engine:
        print("Oracle engine created successfully.")
        #Use oracle_engine...
    else:
        print("Failed to create Oracle engine.")

    #Example of a bad database name.
    bad_engine = engine_creator.create_engine_from_config("bad_db", credentials, config)
    ```

    This example demonstrates how to create a `DatabaseEngineCreator` object, provide database configurations and credentials, and create SQLAlchemy engines for PostgreSQL and Oracle databases. Remember to replace `"your_module.engine_factories"` with the correct import path for your engine factory classes.

# Engine_factories.py

This Python module defines a protocol and concrete classes for creating SQLAlchemy database engines for PostgreSQL and Oracle databases.

## Protocol: DatabaseEngineFactory

### Description

The `DatabaseEngineFactory` protocol defines the interface for classes that create SQLAlchemy engine objects.

### Methods

#### `create_engine(credentials: Dict[str, str]) -> sa.Engine`

* **Description**: Creates a SQLAlchemy engine.
* **Parameters**:
    * `credentials` (Dict[str, str]): A dictionary containing database credentials (username and password).
* **Returns**:
    * `sa.Engine`: A SQLAlchemy engine object.
* **Note**: Concrete classes implementing this protocol must provide specific implementations for creating engines for different database types.

## Class: PostgresEngineFactory

### Description

The `PostgresEngineFactory` class creates SQLAlchemy engine objects for PostgreSQL databases.

### Methods

#### `create_engine(credentials: Dict[str, str], host: str, port: int, database: str) -> sa.Engine`

* **Description**: Creates a PostgreSQL SQLAlchemy engine.
* **Parameters**:
    * `credentials` (Dict[str, str]): A dictionary containing database credentials (username and password).
    * `host` (str): The host address of the PostgreSQL server.
    * `port` (int): The port number of the PostgreSQL server.
    * `database` (str): The name of the PostgreSQL database.
* **Functionality**:
    * Constructs a PostgreSQL connection URL using the provided credentials, host, port, and database name.
    * Uses `sqlalchemy.create_engine()` to create a SQLAlchemy engine from the constructed URL.
* **Returns**:
    * `sa.Engine`: A SQLAlchemy engine object for PostgreSQL.

## Class: OracleEngineFactory

### Description

The `OracleEngineFactory` class creates SQLAlchemy engine objects for Oracle databases.

### Methods

#### `create_engine(credentials: Dict[str, str], host: str, port: int, service_name: str) -> sa.Engine`

* **Description**: Creates an Oracle SQLAlchemy engine.
* **Parameters**:
    * `credentials` (Dict[str, str]): A dictionary containing database credentials (username and password).
    * `host` (str): The host address of the Oracle server.
    * `port` (int): The port number of the Oracle server.
    * `service_name` (str): The service name of the Oracle database.
* **Functionality**:
    * Constructs an Oracle connection URL using the provided credentials, host, port, and service name.
    * Uses `sqlalchemy.create_engine()` to create a SQLAlchemy engine from the constructed URL.
* **Returns**:
    * `sa.Engine`: A SQLAlchemy engine object for Oracle.

## Usage

1.  **Installation**:
    Ensure the `sqlalchemy`, `psycopg2` (for PostgreSQL), and `cx_Oracle` (for Oracle) libraries are installed:

    ```bash
    pip install sqlalchemy psycopg2 cx_Oracle
    ```

2.  **Example**:

    ```python
    import sqlalchemy as sa
    from typing import Protocol, Dict

    class DatabaseEngineFactory(Protocol):
        """Protocol for database engine factories."""

        def create_engine(self, credentials: Dict[str, str]) -> sa.Engine:
            """Creates a SQLAlchemy engine."""

    class PostgresEngineFactory:
        """Creates a PostgreSQL SQLAlchemy engine."""

        def create_engine(self, credentials: Dict[str, str], host: str, port: int, database: str) -> sa.Engine:
            url = f"postgresql+psycopg2://{credentials['username']}:{credentials['password']}@{host}:{port}/{database}"
            return sa.create_engine(url)

    class OracleEngineFactory:
        """Creates an Oracle SQLAlchemy engine."""

        def create_engine(self, credentials: Dict[str, str], host: str, port: int, service_name: str) -> sa.Engine:
            url = f"oracle+cx_oracle://{credentials['username']}:{credentials['password']}@{host}:{port}/?service_name={service_name}"
            return sa.create_engine(url)

    # Example usage:
    credentials = {
        "username": "myuser",
        "password": "mypassword"
    }

    postgres_factory = PostgresEngineFactory()
    postgres_engine = postgres_factory.create_engine(credentials, "localhost", 5432, "mydatabase")

    oracle_factory = OracleEngineFactory()
    oracle_engine = oracle_factory.create_engine(credentials, "192.168.1.100", 1521, "oracleservice")

    if postgres_engine:
        print("PostgreSQL engine created successfully.")
        # Use postgres_engine...
    else:
        print("Failed to create PostgreSQL engine.")

    if oracle_engine:
        print("Oracle engine created successfully.")
        #Use oracle_engine...
    else:
        print("Failed to create Oracle engine.")
    ```

    This example demonstrates how to use `PostgresEngineFactory` and `OracleEngineFactory` to create SQLAlchemy engines
