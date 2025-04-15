import logging
import uuid
from typing import Callable, Generator

from pulseel.utils.models import ExtractionInfo, IncrementalConfig
from pulseel.utils.typing import ExtractionResult
from polars import DataFrame

def ingestion_pipeline(extractor: Callable[..., ExtractionResult],
                       loader: Callable[..., ExtractionInfo],
                       normalizer: Callable[..., Generator[DataFrame, None, None]] | None = None,
                       ) -> ExtractionInfo:
    pipeline_id = uuid.uuid4()
    data_generator  = extractor()

    if normalizer:
        data_generator = normalizer(data_generator)

    info = loader(pipeline_id, data_generator)

    if info.rows_extracted == 0:
        logging.info("No new data to extracted")
        return

    logging.info(f"Extracted {info.rows_extracted} rows from MongoDB in {info.execution_in_seconds} seconds")

    logging.info(
        f"Uploaded {info.rows_extracted} rows to Azure Data Lake"
    )

    return info






