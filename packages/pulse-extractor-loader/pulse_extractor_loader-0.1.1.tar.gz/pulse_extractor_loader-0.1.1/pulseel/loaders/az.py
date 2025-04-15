import datetime
import os
import tempfile
import uuid
from pathlib import Path
from typing import List

import polars as pl

from azure.storage.blob import BlobServiceClient

from pulseel.loaders.filesystem import save_to_folder
from pulseel.utils.models import ADLSConfig, ExtractionInfo
from typing import Generator

from pulseel.utils.typing import ExtractionResult

def upload_to_blob_storage(pipeline_id: uuid.UUID,
                           result: ExtractionResult,
                           path: str, config: ADLSConfig) -> ExtractionInfo:

    with tempfile.TemporaryDirectory() as tmpdir:

        info = save_to_folder(
            pipeline_id=pipeline_id,
            data=result,
            path=Path(tmpdir)
        )

        files_to_upload = [f.name for f in Path(tmpdir).glob("*") if f.is_file()]

        if path.endswith("/"):
            path = path[:-1]
        blob_client = BlobServiceClient.from_connection_string(config.connection_string)
        container_client = blob_client.get_container_client(config.container_name)
        for file in files_to_upload:
            with open(Path(tmpdir).joinpath(file), "rb") as data:
                container_client.upload_blob(os.path.join(path, file), data, overwrite=True)


        return info


