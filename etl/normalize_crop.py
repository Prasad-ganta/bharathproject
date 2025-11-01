# etl/normalize_crop.py
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()

df = pd.read_csv(args.input)
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# Map common column names
colmap = {}
for want in ["state", "district", "year", "crop", "production", "area"]:
    for c in df.columns:
        if want in c:
            colmap[want] = c
            break
df = df.rename(columns=colmap)

if "production" in df.columns:
    df["production"] = pd.to_numeric(df["production"], errors="coerce")
if "year" in df.columns:
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

df.to_csv(args.output, index=False)
print("Wrote normalized crop data to", args.output)

