# User Stories & Acceptance Criteria

## Epic: Report ingestion
- As an analyst, I want to upload a PDF annual report so that I can start reviewing company metrics.
  - Given a PDF is selected, when extraction runs, then the app displays extracted metric fields or a clear error.
- As an analyst, I want to see the reporting period so that I can compare the correct periods.
  - Given the upload form, when I enter a period label, then it appears in the metrics table.

## Epic: Metric validation
- As an analyst, I want to edit extracted values so that I can correct parsing errors.
  - Given extracted metrics, when I edit a cell, then charts and observations use the edited value.

## Epic: Analysis and export
- As an analyst, I want to visualize a selected metric over time so that I can spot trends.
  - Given two or more periods, when I select a metric, then a trend chart is displayed.
- As an analyst, I want to export reviewed metrics so that I can reuse them in a spreadsheet.
  - When I click CSV export, then a CSV file is downloaded.
