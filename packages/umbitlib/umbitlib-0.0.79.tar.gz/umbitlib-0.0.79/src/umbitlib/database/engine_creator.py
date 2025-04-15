import sqlalchemy as sa
from typing import Dict, Optional
from .engine_factories import PostgresEngineFactory, OracleEngineFactory

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