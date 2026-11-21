# Product Requirements Document — Financial Statement Analyzer

## Problem
Analysts often spend time locating recurring financial metrics across lengthy company reports. The prototype aims to reduce manual effort while keeping a human validation step.

## Target users
- Investment and equity research analysts
- Finance students and business analysts
- Founders reviewing company financials

## Goal
Allow a user to upload a text-based annual report, extract selected metrics, validate the values, and inspect period-over-period trends.

## MVP scope
1. PDF upload and text extraction
2. Pattern-based extraction of Revenue, EBITDA, Net Profit, Total Debt and Operating Cash Flow
3. Editable validation table
4. Trend visualization and CSV export
5. Basic rule-based observations

## Out of scope
OCR for scanned PDFs, audited financial interpretation, live data integrations, investment recommendations, multi-company data rooms.

## Success metrics (proposed)
- Metric extraction precision on a curated test set
- Median time to validate five metrics
- Percentage of uploaded reports producing at least three usable metrics
- CSV export completion rate

## Risks
- PDF layouts and labels vary
- Units (₹, $, thousands, millions) may be ambiguous
- Pattern matching may capture the wrong number
- Users may over-trust automated output

## Mitigations
Show a validation step, clearly label limitations, retain source reports outside the app, and require analyst verification.
