from datetime import datetime
import os
from functools import partial

import pytest
from azure.storage.blob import BlobServiceClient
from pymongo import MongoClient
from testcontainers.mongodb import MongoDbContainer

from pulseel.loaders.az import upload_to_blob_storage
from pulseel.pipelines import ingestion_pipeline
from pulseel.pipelines.mongo_to_az import mongo_to_az
from pulseel.utils.models import IncrementalConfig, MongoConfig, ADLSConfig
import polars as pl
import polars.testing as plt


mongo = MongoDbContainer("mongo:latest", dbname="test")

from pulseel.extractors.mongo import get_mongo_data

@pytest.fixture(scope="module", autouse=True)
def setup(request):
    mongo.start()

    client = mongo.get_connection_client()
    db = client.test
    collection = db.data

    collection.insert_many([
        {'_id': 1, 'amount': 21, 'last_updated': datetime(2020, 12, 10, 1, 3, 1),
         'account': {'name': 'Customer1', 'account_number': 1}, 'txns': ['A']},
        {'_id': 2, 'amount': 16, 'last_updated': datetime(2020, 7, 23, 6, 7, 11),
         'account': {'name': 'Customer2', 'account_number': 2}, 'txns': ['A', 'B']},
        {'_id': 3, 'amount': 3, 'last_updated': datetime(2021, 3, 10, 18, 43, 9),
         'account': {'name': 'Customer3', 'account_number': 3}, 'txns': ['A', 'B', 'C']},
        {'_id': 4, 'amount': 0, 'last_updated': datetime(2021, 2, 25, 3, 50, 31),
         'account': {'name': 'Customer4', 'account_number': 4}, 'txns': ['A', 'B', 'C', 'D']}])

    def remove_container():
        mongo.stop()

    request.addfinalizer(remove_container)

    os.environ["MONGO_URI"] = mongo.get_connection_url()

    yield client

def test_mongo_extraction_full():



    iconf = None

    result  = get_mongo_data(os.environ["MONGO_URI"], "test", "data", incremental=iconf)

    df, info = next(result)

    assert df.shape == (4, 5) and info.rows_extracted == 4


def test_mongo_extraction_incremental():

    iconf = IncrementalConfig(column_name="last_updated",
                              last_value=datetime(2020, 12, 10, 1, 3, 1),
                              column_type="timestamp")

    result = get_mongo_data(os.environ["MONGO_URI"], "test", "data", incremental=iconf)

    df, info = next(result)


    assert df.shape == (2, 5) and info.rows_extracted == 2  and info.inc_last_value == datetime(2021, 3, 10, 18, 43, 9)



def test_mongo_to_az(azurite):


    mongo_to_az(os.environ["MONGO_URI"], "test", "data", azurite.get_connection_string(), "test", "data/t1")

    # azconf = ADLSConfig(connection_string=azurite.get_connection_string(), container_name="test")
    #
    # extractor = partial(get_mongo_data, os.environ["MONGO_URI"], "test", "data")
    # loader = partial(upload_to_blob_storage, config=azconf, path="data/t1")
    # info = ingestion_pipeline(extractor,loader)
    #
    #
    # # info = mongo_to_az(mconf, azconf, "data/t1")

    # Test if file exists and is a parquet with correct data
    client = BlobServiceClient.from_connection_string(azurite.get_connection_string())
    container = client.get_container_client("test")
    f = container.list_blobs("data/t1/")

    assert len(list(f)) == 3




