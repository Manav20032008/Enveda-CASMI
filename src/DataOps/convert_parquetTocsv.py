from pathlib import Path
import duckdb

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

train_parquet = DATA_DIR / "train.parquet"
test_parquet = DATA_DIR / "test.parquet"

train_csv = DATA_DIR / "train.csv"
test_csv = DATA_DIR / "test.csv"

for path in (train_parquet, test_parquet):
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}\n" f"Check that your Parquet files are inside {DATA_DIR}")

con = duckdb.connect()
con.execute("SET memory_limit = '6GB'")
con.execute("SET threads = 4")

try:
    for source, destination in [(train_parquet, train_csv),(test_parquet, test_csv),]:
        print(f"\nConverting {source.name} to {destination.name}...")

        source_sql = str(source).replace("'", "''")
        destination_sql = str(destination).replace("'", "''")

        con.execute(f"""
            COPY (
                SELECT *
                FROM read_parquet('{source_sql}')
            )
            TO '{destination_sql}'
            (HEADER, DELIMITER ',')
            """)

        print(f"Saved:{destination}")

    print("\nConversion completed")

finally:
    con.close()
