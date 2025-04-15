from datetime import datetime, timezone
from typing import Union
from dateutil import tz

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

def formatted_utc_now(format="%Y-%m-%d %H:%M:%S") -> str:
    """Retorna timestamp atual em UTC no formato de string.

    :return: Datetime corrente em UTC
    """
    return utc_now().strftime(format)


def to_utc_datetime(_datetime: Union[str, datetime], /, _from: str = "UTC") -> datetime:
    """Converte uma string ou datetime para datetime em UTC.

    Se o datetime não possui informação de timezone, converte para o timezone especificado em `_from`.

    Args:
        _datetime (Union[str, datetime]): Data e hora a ser convertida.
        _from (str): Timezone de origem. (default: 'UTC').
    """
    if isinstance(_datetime, str):
        _datetime = datetime.fromisoformat(_datetime)
    if _datetime.tzinfo is None:
        _datetime = _datetime.replace(tzinfo=tz.gettz(_from))
    return _datetime.astimezone(timezone.utc)


def to_tz_aware(_datetime: Union[datetime, str], _to: str = "UTC", /, _from: str = "UTC") -> datetime:
    """Converte o datetime para o timezone especificado.

    Se o datetime não possui informação de timezone, converte para o timezone especificado em `_from`.

    Args:
        _datetime (Union[str, datetime]): Data e hora a ser convertida.
        timezone (str): Timezone de destino. (default: 'UTC').
        _from (str): Timezone de origem. (default: 'UTC').
    """

    _datetime = to_utc_datetime(_datetime, _from)
    return _datetime.astimezone(tz.gettz(_to))