import enum


class Format(str, enum.Enum):
    PARQUET = "parquet"
    DELTA = "delta"
