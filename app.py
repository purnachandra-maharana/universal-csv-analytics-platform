import os
from pathlib import Path
import streamlit as st
import pandas as pd

from src.loader import load_csv
from src.cleaner import clean_dataset
from src.detector import detect_columns
from src.analyzer import (
    dataset_summary,
    missing_values,
    correlation_matrix
)
from src.visualizer import generate_visualizations
from src.insight_generator import generate_insights
from src.report_generator import create_pdf_report

st.set_page_config(
    page_title="Universal CSV Analytics Platform",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Universal CSV Analytics Platform")
st.markdown(
    "Automated Exploratory Data Analysis (EDA), Data Cleaning, "
    "Correlation Analysis, and PDF Report Synthesis for Any Tabular Dataset."
)

# Sidebar controls
st.sidebar.header("📁 Data Source Selection")
data_source = st.sidebar.radio(
    "Choose data source:",
    ["Upload CSV", "Use Demo Dataset"]
)

df = None
sample_path = Path(__file__).resolve().parent / "data" / "sample_dataset.csv"

if data_source == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader(
        "Upload your CSV file",
        type=["csv"],
        help="Upload any standard comma-separated tabular file"
    )
    if uploaded_file is not None:
        df = load_csv(uploaded_file)
else:
    if sample_path.exists():
        st.sidebar.info("Using bundled entertainment catalog sample dataset.")
        df = pd.read_csv(sample_path)
    else:
        st.sidebar.error("Sample dataset not found.")

if df is not None:
    # Clean dataset
    clean_df = clean_dataset(df)

    # Ensure output folders exist
    os.makedirs("outputs/cleaned_data", exist_ok=True)
    os.makedirs("outputs/charts", exist_ok=True)
    os.makedirs("outputs/reports", exist_ok=True)

    clean_csv_path = "outputs/cleaned_data/cleaned_data.csv"
    clean_df.to_csv(clean_csv_path, index=False)

    st.success("✅ Dataset successfully loaded, cleaned, and normalized.")

    # High-level metrics
    summary = dataset_summary(clean_df)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Rows", summary["Rows"])
    m2.metric("Total Columns", summary["Columns"])
    m3.metric("Missing Values Imputed", summary["Missing Values"])
    m4.metric("Duplicate Rows Dropped", summary["Duplicates"])

    # Tabs for structured inspection
    tab_preview, tab_schema, tab_stats, tab_charts, tab_report = st.tabs([
        "📋 Data Preview",
        "🔍 Schema & Missing Values",
        "📈 Correlation Analysis",
        "🎨 Visualizations",
        "📄 Insights & PDF Report"
    ])

    with tab_preview:
        st.subheader("Cleaned Dataset Preview (First 10 Rows)")
        st.dataframe(clean_df.head(10), use_container_width=True)
        st.download_button(
            label="📥 Download Cleaned CSV",
            data=clean_df.to_csv(index=False),
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )

    with tab_schema:
        st.subheader("Inferred Column Schema")
        detected = detect_columns(clean_df)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Numeric Columns ({len(detected['numeric'])})**")
            st.write(detected["numeric"])
        with c2:
            st.markdown(f"**Categorical Columns ({len(detected['categorical'])})**")
            st.write(detected["categorical"])

        st.subheader("Missing Value Breakdown (Pre-Cleaning Baseline)")
        st.dataframe(missing_values(df), use_container_width=True)

    with tab_stats:
        st.subheader("Correlation Matrix (Numeric Attributes)")
        corr = correlation_matrix(clean_df)
        if not corr.empty and corr.shape[0] > 1:
            st.dataframe(corr.style.background_gradient(cmap="coolwarm"), use_container_width=True)
        else:
            st.info("Insufficient numeric columns to compute multi-variable correlation.")

    with tab_charts:
        st.subheader("Automated Visualization Gallery")
        with st.spinner("Generating statistical distributions and heatmaps..."):
            generate_visualizations(clean_df, "outputs/charts")

        chart_files = sorted([f for f in os.listdir("outputs/charts") if f.endswith(".png")])
        if chart_files:
            grid_cols = st.columns(2)
            for idx, cfile in enumerate(chart_files):
                cpath = os.path.join("outputs/charts", cfile)
                caption = cfile.replace("_", " ").replace(".png", "").title()
                grid_cols[idx % 2].image(cpath, caption=caption, use_container_width=True)
        else:
            st.info("No visualization charts could be generated for this schema.")

    with tab_report:
        st.subheader("Automated Synthesized Insights")
        insights = generate_insights(clean_df)
        for insight in insights:
            st.markdown(f"- {insight}")

        pdf_path = "outputs/reports/report.pdf"
        create_pdf_report(pdf_path, insights)

        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
            st.download_button(
                label="📥 Download Executive PDF Report",
                data=pdf_data,
                file_name="executive_csv_report.pdf",
                mime="application/pdf"
            )

else:
    st.info("👋 Welcome! Upload a CSV file in the left sidebar or select 'Use Demo Dataset' to begin.")
