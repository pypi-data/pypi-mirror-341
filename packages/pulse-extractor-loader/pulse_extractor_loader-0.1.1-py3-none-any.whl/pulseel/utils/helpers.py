from enum import StrEnum

from adlfs import AzureBlobFileSystem
from azure.storage.blob import BlobServiceClient

from pulseel.utils.models import DatabaseConfig, DatabaseType, ADLSConfig



def get_adls_client(conf: ADLSConfig) -> BlobServiceClient:

    # Uses master account key
    if conf.account_key:
        return BlobServiceClient(account_url=conf.account_url, account_key=conf.account_key)

    return AzureBlobFileSystem(conf.account_name, client_id=conf.client_id, client_secret=conf.client_secret, tenant_id=conf.tenant_id)

def get_sqlalchemy_uri(config: DatabaseConfig):

    if config.type == DatabaseType.MSSQL:
        return f"mssql+pymssql://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}"

    if config.type == DatabaseType.POSTGRESQL:
        return f"postgresql:psycopg2//{config.user}:{config.password}@{config.host}:{config.port}/{config.database}"


def get_connectorx_uri(config: DatabaseConfig):

    if config.type == DatabaseType.MSSQL:
        return f"mssql://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}"

    if config.type == DatabaseType.POSTGRESQL:
        return f"postgresql://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}"