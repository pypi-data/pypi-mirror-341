import logging
import os
import tempfile
import uuid
from typing import List
import adlfs
from pulseel.extractors.rdbms.mssql import get_data
from pulseel.loaders.az import upload_to_blob_storage
from pulseel.utils.helpers import get_sqlalchemy_uri
from pulseel.utils.models import DatabaseConfig, ExtractionInfo, IncrementalConfig, ADLSConfig
from sqlalchemy import create_engine



def mssql_to_az(db_conf: DatabaseConfig,
                query: str | List[str],
                az_path: str,
                az_config: ADLSConfig,
                inc_conf: IncrementalConfig | None = None
                ):

    engine = create_engine(get_sqlalchemy_uri(db_conf))

    generator = get_data(engine, query, incremental=inc_conf)

    info = upload_to_blob_storage(generator, az_path, az_config)

    if info.rows_extracted == 0:
        logging.info("No new data to extracted")
        return

    logging.info(f"Extracted {info.rows_extracted} rows from SQLServer in {info.execution_in_seconds} seconds")

    logging.info(
        f"Uploaded {info.rows_extracted} rows to Azure Data Lake at {az_path}"
    )

# TODO Build a argument parsing cli







