# qa_engine/executor.py
import pandas as pd
import os

DATA_SOURCE_CROP = "https://www.data.gov.in/catalog/district-wise-season-wise-crop-production-statistics-0"
DATA_SOURCE_RAIN = "https://www.data.gov.in/resource/sub-divisional-monthly-rainfall-1901-2017"

def _read_table(path_parquet, path_csv):
    # Parquet may not be available; prefer CSV for portability.
    if os.path.exists(path_parquet):
        return pd.read_parquet(path_parquet)
    if os.path.exists(path_csv):
        return pd.read_csv(path_csv)
    raise FileNotFoundError("No data file found: " + str(path_parquet) + " or " + str(path_csv))

def compare_states_avg_rain_and_top_crops(state_x, state_y, n_years=5, top_m=3,
                                         crop_parquet='data/crop_normalized.parquet',
                                         rain_parquet='data/rainfall_normalized.parquet',
                                         crop_csv='data/crop_normalized.csv',
                                         rain_csv='data/rainfall_normalized.csv',
                                         source_urls=None):
    # load tables (CSV fallback)
    if os.path.exists(crop_parquet) or os.path.exists(crop_csv):
        crop = _read_table(crop_parquet, crop_csv)
    else:
        raise FileNotFoundError('Crop data missing. Place normalized crop CSV at data/crop_normalized.csv or parquet.')
    if os.path.exists(rain_parquet) or os.path.exists(rain_csv):
        rain = _read_table(rain_parquet, rain_csv)
    else:
        raise FileNotFoundError('Rainfall data missing. Place normalized rainfall CSV at data/rainfall_normalized.csv or parquet.')
    # Ensure numeric years
    rain['year'] = pd.to_numeric(rain['year'], errors='coerce')
    crop['year'] = pd.to_numeric(crop['year'], errors='coerce')
    years = sorted(rain['year'].dropna().unique().tolist())
    if not years:
        return {'error':'no years in rainfall data'}
    last_years = years[-n_years:]
    rain_sel = rain[rain['year'].isin(last_years) & rain['state'].isin([state_x, state_y])]
    avg_rain = rain_sel.groupby('state')['annual_rainfall_mm'].mean().to_dict()
    # crop top M by sum production
    crop_sel = crop[crop['year'].isin(last_years) & crop['state'].isin([state_x, state_y])]
    top = {}
    for s in [state_x, state_y]:
        df = crop_sel[crop_sel['state']==s]
        if 'crop' in df.columns and 'production' in df.columns:
            agg = df.groupby('crop')['production'].sum().reset_index().sort_values('production', ascending=False)
            records = agg.head(top_m).to_dict(orient='records')
            top[s] = records
        else:
            top[s] = []
    result = {
        'avg_rain': avg_rain,
        'top_crops': top,
        'years_used': last_years,
        'sources': {
            'crop_resource_page': DATA_SOURCE_CROP,
            'rain_resource_page': DATA_SOURCE_RAIN
        }
    }
    return result

def compose_answer(result_dict):
    if 'error' in result_dict:
        return result_dict['error']
    yrs = result_dict.get('years_used', [])
    if not yrs:
        return "No years available."
    s = f"Average annual rainfall for years {yrs[0]} to {yrs[-1]}:\n"
    for st, val in result_dict['avg_rain'].items():
        s += f"- {st}: {val:.1f} mm (source: {result_dict['sources']['rain_resource_page']})\n"
    s += "\nTop crops by total production in the same period:\n"
    for st, rows in result_dict['top_crops'].items():
        s += f"{st}:\n"
        if rows:
            for r in rows:
                prod = r.get('production', 0)
                s += f"  - {r.get('crop')}: {prod} (source: {result_dict['sources']['crop_resource_page']})\n"
        else:
            s += "  - No data\n"
    return s

