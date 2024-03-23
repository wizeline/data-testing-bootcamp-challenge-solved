from pathlib import Path

import duckdb
import pandas
import pytest
from pandas.testing import assert_frame_equal

from qa_challenge.constants import SQL_FOLDER


class TestSql:
    @pytest.mark.parametrize(
        "query_name", ["most_interacted_videos_per_country", "avg_age_by_gender"]
    )
    def test_avg_user_consumption(
        self, query_name: str, assets_folder: Path, db: duckdb.DuckDBPyConnection
    ):
        # Path: tests/sql/test_query.py
        # Compare this snippet from qa_challenge/constants.py:
        # from pathlib import Path
        #
        # SQL_FOLDER = Path(__file__).parent / "sql"
        # 1. Read sql file from folder
        sql_file = SQL_FOLDER / f"{query_name}.sql"
        with open(sql_file, "r", encoding="utf-8") as f:
            query = f.read()

        # 2. Execute query and fetch result
        result = db.execute(query).fetchdf()

        # 3. Read expected result
        expected = pandas.read_csv(assets_folder / "result" / f"{query_name}.csv")

        # 4. Assert result
        assert_frame_equal(result, expected, check_dtype=False)
