import os
import uuid
from pathlib import Path
from typing import List

from pulseel.utils.models import ExtractionInfo
from pulseel.utils.typing import ExtractionResult


def save_to_folder(pipeline_id: uuid.UUID,
                   data: ExtractionResult,
                   path: Path
                   ):

    path.mkdir(parents=True, exist_ok=True)
    info_list: List[ExtractionInfo] = []

    with open(path.joinpath(f"{pipeline_id}__started"), "w") as f:
        f.write("")

    for i, data in enumerate(data):
        df = data[0]
        info_list.append(data[1])
        filename = f"{pipeline_id}-{i}.parquet"
        abs_path = path.joinpath(filename)
        with open(abs_path, "wb") as f:
            df.write_parquet(f)

    sum_exec_time = sum([e.execution_in_seconds for e in info_list])
    sum_rows = sum([e.rows_extracted for e in info_list])
    max_inc_value = max([e.inc_last_value for e in info_list])

    with open(path.joinpath(f"{pipeline_id}__completed"), "w") as f:
        f.write("")

    return ExtractionInfo(rows_extracted=sum_rows, execution_in_seconds=sum_exec_time, inc_last_value=max_inc_value)