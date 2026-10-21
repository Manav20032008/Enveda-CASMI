from pathlib import Path
import duckdb
import pandas as pd

# Set paths relative to the current working directory
DATA = Path.cwd() / "data"

train_path = DATA / "train.parquet"
test_path = DATA / "test.parquet"
sample_path = DATA / "sample_submission.csv"

for path in [train_path, test_path, sample_path]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

con = duckdb.connect()
con.execute("SET memory_limit = '6GB'")
con.execute("SET threads = 4")

# Inspect the schema without loading the whole dataset
schema = con.execute(
    "DESCRIBE SELECT * FROM read_parquet(?)",
    [str(train_path)]
).df()

print("TRAIN SCHEMA")
print(schema.to_string(index=False))

# Load only the small sample submission
sample = pd.read_csv(sample_path)
print("\nSample submission:", sample.shape)
print(sample.head(3).to_string(index=False))

# Aggregate statistics inside DuckDB
stats = con.execute("""
    SELECT
        COUNT(*) AS spectra,
        COUNT(DISTINCT molecule_id) AS molecule_ids,
        COUNT(DISTINCT inchikey14) AS unique_structures
    FROM read_parquet(?)
""", [str(train_path)]).df()

print("\nTRAIN STATISTICS")
print(stats.to_string(index=False))

# Inspect source-library coverage
sources = con.execute("""
    SELECT
        ingest_lib,
        COUNT(*) AS spectra,
        COUNT(DISTINCT inchikey14) AS structures
    FROM read_parquet(?)
    GROUP BY ingest_lib
    ORDER BY spectra DESC
""", [str(train_path)]).df()

print("\nSOURCE LIBRARIES")
print(sources.to_string(index=False))