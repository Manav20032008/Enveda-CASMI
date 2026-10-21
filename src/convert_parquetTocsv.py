
from pathlib import Path
import duckdb

DATA = Path.cwd() / "data"

con = duckdb.connect()
con.execute("SET memory_limit = '6GB'")
con.execute("SET threads = 4")

for filename in ["train", "test"]:
    parquet_path = DATA / f"{filename}.parquet"
    csv_path = DATA / f"{filename}.csv"

    if not parquet_path.exists():
        raise FileNotFoundError(parquet_path)

    print(f"Converting {parquet_path.name}...")

    con.execute(
        """
        COPY (
            SELECT *
            FROM read_parquet(?)
        )
        TO ?
        (FORMAT CSV, HEADER TRUE)
        """,
        [str(parquet_path), str(csv_path)],
    )

    print(f"Saved: {csv_path}")

con.close()
print("Conversion complete!")
