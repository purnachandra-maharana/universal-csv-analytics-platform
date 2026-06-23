
import streamlit as st
import pandas as pd
import os

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

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file:

    # Load
    df = load_csv(uploaded_file)

    # Clean
    clean_df = clean_dataset(df)

    # Save cleaned data
    os.makedirs(
        "outputs/cleaned_data",
        exist_ok=True
    )

    clean_df.to_csv(
        "outputs/cleaned_data/cleaned_data.csv",
        index=False
    )

    st.success("Dataset Loaded & Cleaned")

    st.subheader("Preview")

    st.dataframe(clean_df.head())

    # Summary
    summary = dataset_summary(clean_df)

    col1,col2,col3,col4 = st.columns(4)

    col1.metric(
        "Rows",
        summary["Rows"]
    )

    col2.metric(
        "Columns",
        summary["Columns"]
    )

    col3.metric(
        "Missing Values",
        summary["Missing Values"]
    )

    col4.metric(
        "Duplicates",
        summary["Duplicates"]
    )

    # Column Detection
    detected = detect_columns(
        clean_df
    )

    st.subheader(
        "Detected Columns"
    )

    st.write(detected)

    # Missing Values
    st.subheader(
        "Missing Value Analysis"
    )

    st.dataframe(
        missing_values(clean_df)
    )

    # Correlation
    st.subheader(
        "Correlation Matrix"
    )

    st.dataframe(
        correlation_matrix(clean_df)
    )

    # Generate Charts
    generate_visualizations(
        clean_df,
        "outputs/charts"
    )

    st.success(
        "Charts Generated"
    )

    # Insights
    insights = generate_insights(
        clean_df
    )

    st.subheader(
        "Insights"
    )

    for insight in insights:

        st.write(
            "✅",
            insight
        )

    # PDF Report
    os.makedirs(
        "outputs/reports",
        exist_ok=True
    )

    create_pdf_report(
        "outputs/reports/report.pdf",
        insights
    )

    st.success(
        "PDF Report Generated"
    )

    # Download CSV
    st.download_button(
        "Download Cleaned CSV",
        clean_df.to_csv(
            index=False
        ),
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

else:

    st.info(
        "Upload a CSV file to begin."
    )
