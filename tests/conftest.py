from pathlib import Path

import duckdb
import pandas
import pytest


@pytest.fixture(scope="session")
def assets_folder() -> Path:
    return Path(__file__).parent / "assets"


@pytest.fixture(scope="module")
def db(assets_folder: Path) -> duckdb.DuckDBPyConnection:
    with duckdb.connect(":memory:") as conn:
        for dataset in (assets_folder / "source").glob("*.csv"):
            table_name = dataset.stem
            df = pandas.read_csv(dataset)
            conn.register(table_name, df)

        yield conn  # type: ignore
