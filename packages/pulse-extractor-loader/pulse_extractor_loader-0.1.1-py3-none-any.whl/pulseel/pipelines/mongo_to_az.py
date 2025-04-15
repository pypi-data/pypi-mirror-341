import logging
import os
import tempfile
import uuid
from dataclasses import dataclass
from functools import partial

import adlfs
from typing_extensions import Annotated

from pulseel.extractors.mongo import get_mongo_data
from pulseel.loaders.az import upload_to_blob_storage
from pulseel.pipelines import ingestion_pipeline
from pulseel.utils.helpers import get_adls_client
from pulseel.utils.models import MongoConfig, ADLSConfig, ExtractionInfo, IncrementalConfig

import typer

def parse_incremental_config(column_name: str, column_type: str, last_value: str) -> IncrementalConfig:
    return IncrementalConfig(column_name=column_name, column_type=column_type, last_value=last_value)

@dataclass
class PipelineConfig:
    uri: str
    db: str
    collection: str
    az_conn_string: str
    az_container_name: str
    az_path: str

    @classmethod
    def from_env(cls, **overrides):
        """Create config from environment variables with optional overrides."""
        config = {
            'uri': os.getenv('MONGO_URI'),
            'db': os.getenv('MONGO_DB'),
            'collection': os.getenv('MONGO_COLLECTION'),
            'az_conn_string': os.getenv('AZURE_CONNECTION_STRING'),
            'az_container_name': os.getenv('AZURE_CONTAINER_NAME'),
            'az_path': os.getenv('AZURE_PATH', 'default/path')
        }

        # Override with any provided values
        config.update({k: v for k, v in overrides.items() if v is not None})

        # Check for missing required values
        missing = [k for k, v in config.items() if v is None and k != 'az_path']
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        return cls(**config)

def mongo_to_az(uri: str,
                db: str,
                collection: str,
                az_conn_string: str,
                az_container_name: str,
                az_path: str,
                inc_config: Annotated[IncrementalConfig , typer.Option(parser=parse_incremental_config)] = None):

    config = PipelineConfig.from_env(
        uri=uri,
        db=db,
        collection=collection,
        az_conn_string=az_conn_string,
        az_container_name=az_container_name,
        az_path=az_path
    )

    extractor = partial(get_mongo_data, config.uri, config.db, config.collection, incremental=inc_config)
    loader = partial(
        upload_to_blob_storage,
        config=ADLSConfig(config.az_conn_string, config.az_container_name),
        path=config.az_path
    )
    info = ingestion_pipeline(extractor, loader)


if __name__ == "__main__":
    typer.run(mongo_to_az)
