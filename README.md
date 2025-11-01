# OGD QnA Prototype

A Question-Answering system prototype for Open Government Data (OGD), focusing on Agriculture and Climate data from data.gov.in.

## Features

- Natural Language Understanding (NLU) for parsing questions
- Query planning and execution engine
- Data normalization pipelines
- Interactive Streamlit web interface
- Source attribution for all answers

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your data.gov.in CSV resource URLs
```

3. Fetch data:
```bash
python fetch_crop.py
python fetch_rainfall.py
```

4. Normalize data:
```bash
python etl/normalize_crop.py --input data/crop_production.csv --output data/crop_normalized.csv
python etl/normalize_rainfall.py --input data/rainfall_state_annual.csv --output data/rainfall_normalized.csv
```

5. Run the webapp:
```bash
streamlit run webapp/app.py
```

## Architecture

- **NLU** (`qa_engine/nlu.py`): Extracts entities (states, crops, years, intent) from questions
- **Planner** (`qa_engine/planner.py`): Determines data sources needed
- **Executor** (`qa_engine/executor.py`): Executes queries using Pandas
- **Webapp** (`webapp/app.py`): Streamlit interface for interactive Q&A

## Data Sources

- Crop Production: https://www.data.gov.in/catalog/district-wise-season-wise-crop-production-statistics-0
- Rainfall: https://www.data.gov.in/resource/sub-divisional-monthly-rainfall-1901-2017

