from pathlib import Path
import pandas as pd
import math

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

input_file = DATA_DIR / "train.csv"
output_dir = DATA_DIR / "train_parts"
output_dir.mkdir(parents=True, exist_ok=True)

print("Counting rows...")
total_rows = sum(len(chunk) for chunk in pd.read_csv(input_file, chunksize=100_000))
rows_per_part = math.ceil(total_rows / 6)

print(f"Total rows: {total_rows:,}")
print(f"Rows per part: {rows_per_part:,}")

part_number = 1
for part_number in range(1,7):
    
    output_file = output_dir / f"train{part_number}.csv"
    start_row = (part_number - 1) * rows_per_part
    
    
    remaining = min(rows_per_part, total_rows - start_row)
    if remaining <= 0:
        break


    print(f"Creating {output_file.name}...")
    reader = pd.read_csv(input_file,chunksize=100_000,skiprows=range(1, start_row + 1) if start_row else None,nrows=remaining)

    first_chunk = True
    for chunk in reader:
        chunk.to_csv(output_file,mode="w" if first_chunk else "a",index=False,header=first_chunk)
        first_chunk = False

print("Files Created.")
