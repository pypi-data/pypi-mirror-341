from dataclasses import dataclass
from enum import StrEnum

class DatabaseType(StrEnum):
    MSSQL = "mssql"
    POSTGRESQL = "postgresql"


@dataclass
class MongoConfig:
    uri: str
    db: str
    collection: str


@dataclass
class ADLSConfig:
    connection_string: str
    container_name: str


@dataclass
class DatabaseConfig:
    user: str
    password: str
    host: str
    port: int
    database: str
    type: DatabaseType


@dataclass
class ExtractionInfo:
    rows_extracted: int
    execution_in_seconds: int
    inc_last_value: str = "-1"


@dataclass
class IncrementalConfig:
    column_name: str
    column_type: str
    last_value: str
