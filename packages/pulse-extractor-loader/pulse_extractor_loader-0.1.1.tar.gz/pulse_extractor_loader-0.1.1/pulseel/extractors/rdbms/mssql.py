from datetime import datetime
from enum import Enum
from typing import Tuple, Union, List, Any, Generator
import polars as pl
import sqlalchemy.engine
import sqlparse
from polars import DataFrame

from pulseel.utils.datetimes import to_tz_aware
from pulseel.utils.models import ExtractionInfo, IncrementalConfig
from pulseel.utils.typing import ExtractionResult


class CdcRelationalOperator(str, Enum):
    """Enumeration of the possible relational operators for
    `sys.fn_cdc_map_time_to_lsn` function.

    Possible values:
    - `largest less than`
    - `largest less than or equal`
    - `smallest greater than`
    - `smallest greater than or equal`
    """

    LARGEST_LESS_THAN = "largest less than"
    LARGEST_LESS_THAN_OR_EQUAL = "largest less than or equal"
    SMALLEST_GREATER_THAN = "smallest greater than"
    SMALLEST_GREATER_THAN_OR_EQUAL = "smallest greater than or equal"


def py_hexbin_to_mssql(binary_value: str) -> str:
    """Retorn clausula de conversão a representação hexadecimal para binary do
    SQL Server."""

    return f"CONVERT(BINARY(10),'0x{binary_value[2:] if binary_value.startswith('0x') else binary_value}',1)"


def map_time_to_lsn(
    relational_operator: CdcRelationalOperator,
    timestamp: Union[str, datetime],
    tzinfo: str = "UTC",
) -> str:
    """Retorna a cláusula de conversão de timestamp para LSN do SQL Server.

    Args:
        relational_operator (CdcRelationalOperator): Operador relacional.
        timestamp (Union[str, datetime]): Timestamp a ser convertido.
        tzinfo (str): Timezone para conversão da data. (default: 'UTC').
    """

    tz_aware_timestamp = to_tz_aware(timestamp, tzinfo).replace(tzinfo=None)
    timestamp = tz_aware_timestamp.isoformat(" ", "milliseconds")
    return f"sys.fn_cdc_map_time_to_lsn('{relational_operator}', '{timestamp}')"


def get_schema_from_query(engine: sqlalchemy.engine.Engine, query: str) -> pl.DataFrame:
    return pl.read_database(f"SELECT * FROM ({query}) as schema_query WHERE 1=0", engine)


def normalize_query(engine: sqlalchemy.engine.Engine, query: str, ) -> str:
    schema = get_schema_from_query(engine, query)
    selectables: list[str] = []
    for col, type in zip(schema.columns, schema.dtypes):
        if col.lower().endswith("rowversion"):
            selectables.append(f"CAST({col} AS BIGINT) AS {col}")
        else:
            selectables.append(col)

    return sqlparse.format(f"SELECT {', '.join(selectables)} FROM ({query}) as query")



def get_data(engine: sqlalchemy.engine.Engine,
             query: str | List[str],
             incremental: IncrementalConfig | None = None
             ) -> ExtractionResult:


    if not isinstance(query, list):
        query = [query]

    for q in query:
        start = datetime.now()
        q = normalize_query(engine, q)
        if incremental:
            q = sqlparse.format(f"SELECT * FROM ({q}) tp_inc WHERE {incremental.column_name} > {incremental.last_value}")
        df = pl.read_database(q, engine, infer_schema_length=None)
        end = datetime.now()
        exec_time = int((end - start).total_seconds())
        rows, _ = df.shape

        last_value = df.select(pl.col(incremental.column_name).max())[0, 0] if incremental else -1

        yield df.write_json()


