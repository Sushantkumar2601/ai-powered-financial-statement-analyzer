# Financial Statement Analyzer

A portfolio-ready Streamlit prototype for extracting selected financial metrics from annual-report PDFs, reviewing extracted values, comparing periods, and generating simple trend observations.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Features
- Demo dataset to explore immediately (fictional figures).
- PDF text extraction for Revenue, EBITDA, Net Profit, Total Debt and Operating Cash Flow.
- Editable metric table so users can validate extraction.
- Trend chart, basic calculated observations and CSV export.

## Limitations
PDF extraction is pattern-based; complex tables, scanned PDFs and inconsistent labels may not parse correctly. OCR and LLM-based extraction are not included. Always verify figures against the source report. This is an educational prototype, not investment advice.

## Product artifacts
See `docs/PRD.md`, `docs/USER_STORIES.md`, and `docs/ROADMAP.md`.
