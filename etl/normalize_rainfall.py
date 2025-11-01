# etl/normalize_rainfall.py
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()

df = pd.read_csv(args.input)
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# find rainfall column (contains 'rain' or 'precip')
found = None
for c in df.columns:
    if "rain" in c or "precip" in c:
        found = c
        break
if found:
    df = df.rename(columns={found: "annual_rainfall_mm"})

if "annual_rainfall_mm" in df.columns:
    df["annual_rainfall_mm"] = pd.to_numeric(df["annual_rainfall_mm"], errors="coerce")
if "year" in df.columns:
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

df.to_csv(args.output, index=False)
print("Wrote normalized rainfall data to", args.output)

