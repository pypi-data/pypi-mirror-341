from polars import DataFrame
from pulseel.utils.models import ExtractionInfo
from typing import Generator, Tuple

ExtractionResult = Generator[Tuple[DataFrame, ExtractionInfo], None, None]