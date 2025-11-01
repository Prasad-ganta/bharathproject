# fetch_rainfall.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("RAINFALL_RESOURCE_URL")
out = "data/rainfall_state_annual.csv"

if not url:
    print("Set RAINFALL_RESOURCE_URL in .env (direct CSV link from data.gov.in resource).")
else:
    print("Downloading rainfall CSV from:", url)
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    os.makedirs("data", exist_ok=True)
    with open(out, "wb") as f:
        f.write(r.content)
    print("Saved:", out)

