import json
from typing import Dict


class DatabaseConfigLoader:
    """Loads and validates database configuration from a JSON file."""

    def validate_database_config(self, config: Dict[str, Dict]) -> None:
        """
        Validates the database configuration to ensure it is correct.
        Raises ValueError if the configuration is invalid.
        """
        required_keys = {"type", "host", "port", "database"}
        for db_name, db_config in config.items():
            if not isinstance(db_config, dict):
                raise ValueError(f"Configuration for '{db_name}' must be a dictionary.")
            missing_keys = required_keys - db_config.keys()
            if missing_keys:
                raise ValueError(f"Configuration for '{db_name}' is missing keys: {missing_keys}")
            if db_config["type"] not in {"postgres", "oracle"}:
                raise ValueError(f"Unsupported database type '{db_config['type']}' for '{db_name}'.")
            if not isinstance(db_config["port"], int):
                raise ValueError(f"Port for '{db_name}' must be an integer.")
            
    def load_database_config(self, config_file: str) -> Dict[str, Dict]:
        """Loads and validates database configuration from a JSON file."""
        with open(config_file, "r") as f:
            config = json.load(f)["databases"]
        self.validate_database_config(config)
        return config