from .credential_provider import CredentialProvider
from .config_loader import DatabaseConfigLoader
from .engine_creator import DatabaseEngineCreator
from .db_interactions import DatabaseInteraction

DB_CONFIG_PATH = r"C:\Cloud\Box\UMB_DataScience\Configs\db_config.json"

class SqlHandler():
    """
    A class to handle SQL database connections and interactions.
    This class provides functionality to establish a connection to a database
    using either a default configuration or a custom configuration file. It also
    initializes a database interaction object for executing queries.
    
    Attributes:
        service_name (str): The name of the database service.
        username (str, optional): The username for authentication. Defaults to None.
        _credentials (dict): The credentials retrieved from the keyring.
        engine (object): The database engine used for connections.
        db_interaction (DatabaseInteraction): An object for interacting with the database.
    
    Methods:
        connect_from_config():
            Establishes a database connection using the default configuration.
        connect_from_custom_config(config_path):
            Establishes a database connection using a custom configuration file.
    
    Example Configuration:
        The configuration dictionary loaded from the JSON file must have the following structure:
        {
            "databases": {
                "database_name": {
                    "type": "postgres",  # or "oracle"
                    "host": "hostname_or_ip",
                    "port": 5432,  # or 1521 for Oracle
                    "database": "database_name"  # For Oracle, this can be the service name
                }
            }
        }
    """
    def __init__(self, service_name: str, username: str=None, custom_config_path: str=None):
        self.service_name = service_name
        self.username = username
        self._credentials = CredentialProvider().get_keyring_credentials(self.service_name, self.username)
        if custom_config_path:
            self.engine = self.connect_from_custom_config(custom_config_path) 
        else:
            self.engine = self.connect_from_config()
        self.db_interaction = DatabaseInteraction(self.engine)

    def connect_from_config(self):
        config = DatabaseConfigLoader().load_database_config(DB_CONFIG_PATH)
        engine = DatabaseEngineCreator().create_engine_from_config(self.service_name, self._credentials, config)
        return engine
    
    def connect_from_custom_config(self, config_path):
        config = DatabaseConfigLoader().load_database_config(config_path)
        engine = DatabaseEngineCreator().create_engine_from_config(self.service_name, self._credentials, config)
        return engine