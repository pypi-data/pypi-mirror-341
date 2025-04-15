import logging
import tempfile
from datetime import datetime
from enum import Enum, StrEnum
from typing import Tuple, Generator, Union

import pyarrow
import pymongo as mongo
import polars as pl
from polars import DataFrame, Series

from pymongoarrow.api import Schema, find_polars_all

from pulseel.utils.models import IncrementalConfig, ExtractionInfo
from pulseel.utils.typing import ExtractionResult
from tempfile import TemporaryDirectory



def get_arrow_type_from_string(type_str: str) -> Union[
    pyarrow.string(),
    pyarrow.int64(),
    pyarrow.float64(),
    pyarrow.bool_(),
    pyarrow.timestamp("ms")]:

    if type_str == "string":
        return pyarrow.string()
    elif type_str == "int":
        return pyarrow.int64()
    elif type_str == "float":
        return pyarrow.float64()
    elif type_str == "boolean":
        return pyarrow.bool_()
    elif type_str == "timestamp":
        return pyarrow.timestamp("ms")


def get_mongo_data(mongo_uri: str,
                   database: str,
                   collection: str,
                   schema: dict | None = None,
                   incremental: IncrementalConfig | None = None,
                   chunk_size: int = 200000,
                   **kwargs
                   ) -> ExtractionResult:
    client = mongo.MongoClient(mongo_uri)
    db = client[database]
    collection = db[collection]

    iop = {incremental.column_name: {"$gt": incremental.last_value}} if incremental else {}

    # Get Number of Documents
    row_count = collection.count_documents(filter=iop)

    logging.info(f"Found {row_count} documents in this query.")

    # Generate chunk intervals
    chunks = [(i, min(i + chunk_size, row_count)) for i in range(0, row_count, chunk_size)]
    logging.info(f"Generated {len(chunks)} batches for chunking.")

    if schema:
        schema = Schema({k: get_arrow_type_from_string(v) for k, v in schema.items()})

    tempdir = tempfile.TemporaryDirectory()
    # Iterate over chunks

    for i, c in enumerate(chunks):
        stime = datetime.now()
        df = find_polars_all(collection, query=iop, schema=schema, limit=chunk_size, skip=c[0])
        last_value = df.select(pl.col(incremental.column_name).max())[0, 0] if incremental else -1
        etime = datetime.now()
        exec_time = int((etime - stime).total_seconds())
        yield df, ExtractionInfo(rows_extracted=row_count, execution_in_seconds=exec_time,
                                 inc_last_value=last_value)
