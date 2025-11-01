# fetch_crop.py
# Download crop CSV from CROP_RESOURCE_URL set in .env
import os
import requests
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("CROP_RESOURCE_URL")
out = "data/crop_production.csv"

if not url:
    print("Set CROP_RESOURCE_URL in .env (direct CSV link from data.gov.in resource).")
else:
    print("Downloading crop CSV from:", url)
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    os.makedirs("data", exist_ok=True)
    with open(out, "wb") as f:
        f.write(r.content)
    print("Saved:", out)

