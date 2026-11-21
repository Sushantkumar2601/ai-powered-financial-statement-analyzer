import re
import io
import pandas as pd
import streamlit as st
import plotly.express as px
from pypdf import PdfReader

st.set_page_config(page_title="Financial Statement Analyzer", page_icon="📊", layout="wide")
st.title("📊 AI-Assisted Financial Statement Analyzer")
st.caption("Upload a financial report or use the demo dataset to extract key metrics and review financial trends.")

METRICS = {
    "Revenue": [r"revenue(?: from operations)?", r"total income"],
    "EBITDA": [r"ebitda", r"earnings before interest, tax, depreciation and amorti[sz]ation"],
    "Net Profit": [r"net profit", r"profit after tax", r"PAT"],
    "Total Debt": [r"total debt", r"borrowings", r"total borrowings"],
    "Cash Flow": [r"net cash from operating activities", r"cash flow from operations"]
}

def extract_pdf_text(file):
    reader = PdfReader(file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def extract_metrics(text):
    results = {}
    for metric, patterns in METRICS.items():
        value = None
        for pattern in patterns:
            match = re.search(pattern + r"[^0-9\-]{0,50}(-?\(?\d[\d,]*(?:\.\d+)?\)?)", text, re.I)
            if match:
                raw = match.group(1).replace(",", "").replace("(", "-").replace(")", "")
                try:
                    value = float(raw)
                except ValueError:
                    pass
                if value is not None:
                    break
        results[metric] = value
    return results

def build_insights(df):
    insights = []
    for metric in ["Revenue", "EBITDA", "Net Profit", "Total Debt", "Cash Flow"]:
        vals = df[metric].dropna().tolist()
        if len(vals) >= 2:
            change = vals[-1] - vals[-2]
            pct = (change / abs(vals[-2]) * 100) if vals[-2] else None
            if pct is not None:
                direction = "increased" if change >= 0 else "decreased"
                insights.append(f"{metric} {direction} by {abs(pct):.1f}% between the two latest periods.")
    if not insights:
        insights.append("Add at least two reporting periods with numeric values to generate trend insights.")
    if "Net Profit" in df and "Revenue" in df:
        latest = df.dropna(subset=["Net Profit", "Revenue"]).tail(1)
        if not latest.empty and latest.iloc[0]["Revenue"]:
            margin = latest.iloc[0]["Net Profit"] / latest.iloc[0]["Revenue"] * 100
            insights.append(f"Latest available net profit margin is {margin:.1f}%.")
    return insights

st.sidebar.header("Input")
mode = st.sidebar.radio("Choose input", ["Demo data", "Upload PDF"])
if mode == "Demo data":
    df = pd.DataFrame([
        {"Period":"FY2023","Revenue":1250,"EBITDA":210,"Net Profit":105,"Total Debt":380,"Cash Flow":160},
        {"Period":"FY2024","Revenue":1480,"EBITDA":265,"Net Profit":142,"Total Debt":350,"Cash Flow":195},
        {"Period":"FY2025","Revenue":1720,"EBITDA":320,"Net Profit":181,"Total Debt":315,"Cash Flow":230},
    ])
    st.info("Demo figures are fictional and provided only to demonstrate the workflow.")
else:
    uploaded = st.sidebar.file_uploader("Upload annual report PDF", type=["pdf"])
    period = st.sidebar.text_input("Reporting period", "FY2025")
    if uploaded:
        try:
            text = extract_pdf_text(uploaded)
            found = extract_metrics(text)
            df = pd.DataFrame([{"Period":period, **found}])
            st.success("PDF text extracted. Review all extracted values before using them.")
            st.caption("PDF extraction is pattern-based and may miss tables or misread figures. Verify against the source report.")
        except Exception as exc:
            st.error(f"Could not read this PDF: {exc}")
            st.stop()
    else:
        st.warning("Upload a PDF to begin, or select Demo data.")
        st.stop()

st.subheader("Financial metrics")
edited = st.data_editor(df, use_container_width=True, num_rows="dynamic")
numeric_cols = [c for c in edited.columns if c != "Period"]
available = [c for c in numeric_cols if pd.to_numeric(edited[c], errors="coerce").notna().any()]
if available:
    selected = st.selectbox("Metric to visualize", available)
    chart_df = edited[["Period", selected]].copy()
    chart_df[selected] = pd.to_numeric(chart_df[selected], errors="coerce")
    st.plotly_chart(px.line(chart_df, x="Period", y=selected, markers=True, title=f"{selected} trend"), use_container_width=True)
else:
    st.info("No numeric metrics found yet. Enter values in the table to visualize them.")

st.subheader("Analyst-style observations")
for item in build_insights(edited):
    st.write("• " + item)

st.subheader("Product notes")
st.write("This prototype demonstrates document ingestion, metric extraction, editable validation, trend visualization and explainable observations. It does not provide investment advice.")
csv = edited.to_csv(index=False).encode("utf-8")
st.download_button("Download reviewed metrics (CSV)", csv, "financial_metrics.csv", "text/csv")
