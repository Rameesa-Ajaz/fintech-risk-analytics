# Fintech Risk Analytics Dashboard

![Fintech Dashboard Preview](docs/dashboard_preview.png)

A dashboard built with Streamlit to visualize credit card transaction risk.

## Project Structure
- `data/`: Contains the raw and cleaned CSV datasets.
- `scripts/`: Data processing scripts.
- `sql/`: SQL queries for risk analysis.
- `dashboard/`: Streamlit dashboard application.
- `docs/`: Documentation and data dictionary.

## How to Run
1. Run data cleaning script: `python scripts/clean_data.py`
2. Launch Streamlit dashboard: `python -m streamlit run dashboard/app.py`
