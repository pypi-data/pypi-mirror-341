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

    def create_engine(self, credentials: Dict[str, str], host: str, port: int, service_name) -> sa.Engine:
        url = f"oracle+oracledb://{credentials['username']}:{credentials['password']}@{host}:{port}/?service_name={service_name}"
        return sa.create_engine(url)