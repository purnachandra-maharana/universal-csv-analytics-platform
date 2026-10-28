import os
import io
import tempfile
import pandas as pd
import pytest

from src.loader import load_csv
from src.cleaner import clean_dataset
from src.detector import detect_columns
from src.analyzer import dataset_summary, missing_values, correlation_matrix
from src.insight_generator import generate_insights
from src.report_generator import create_pdf_report
from src.visualizer import generate_visualizations


@pytest.fixture
def sample_df():
    data = {
        "id": [1, 2, 3, 4, 4],  # duplicate row 4
        "name": ["Alpha", "Beta", "Gamma", "Delta", "Delta"],
        "age": [25.0, None, 35.0, 40.0, 40.0],
        "department": ["Eng", "HR", "Eng", None, None],
        "all_null": [None, None, None, None, None]
    }
    return pd.DataFrame(data)


def test_load_csv():
    csv_data = "a,b,c\n1,2,3\n4,5,6\n"
    buffer = io.StringIO(csv_data)
    df = load_csv(buffer)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 3)
    assert list(df.columns) == ["a", "b", "c"]


def test_clean_dataset(sample_df):
    clean_df = clean_dataset(sample_df)
    # Check duplicate row 4 was removed (5 rows -> 4 rows)
    assert len(clean_df) == 4
    # Check all_null column was dropped
    assert "all_null" not in clean_df.columns
    # Check numeric imputation (median of [25, 35, 40] is 35.0)
    assert not clean_df["age"].isnull().any()
    assert clean_df.loc[sample_df["name"] == "Beta", "age"].values[0] == 35.0
    # Check categorical imputation (mode is "Eng")
    assert not clean_df["department"].isnull().any()


def test_detect_columns(sample_df):
    detected = detect_columns(sample_df)
    assert "id" in detected["numeric"]
    assert "age" in detected["numeric"]
    assert "name" in detected["categorical"]
    assert "department" in detected["categorical"]


def test_dataset_summary(sample_df):
    summary = dataset_summary(sample_df)
    assert summary["Rows"] == 5
    assert summary["Columns"] == 5
    assert summary["Missing Values"] >= 7
    assert summary["Duplicates"] == 1


def test_missing_values(sample_df):
    mv = missing_values(sample_df)
    assert mv["all_null"] == 5
    assert mv["age"] == 1


def test_correlation_matrix():
    df = pd.DataFrame({
        "x": [1, 2, 3, 4, 5],
        "y": [2, 4, 6, 8, 10],
        "label": ["a", "b", "c", "d", "e"]
    })
    corr = correlation_matrix(df)
    assert corr.shape == (2, 2)
    assert pytest.approx(corr.loc["x", "y"], 0.01) == 1.0


def test_generate_insights(sample_df):
    insights = generate_insights(sample_df)
    assert isinstance(insights, list)
    assert len(insights) >= 4
    assert any("5 rows" in s for s in insights)


def test_create_pdf_report():
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, "test_report.pdf")
        insights = ["Insight line 1", "Insight line 2"]
        create_pdf_report(pdf_path, insights)
        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 500


def test_generate_visualizations():
    with tempfile.TemporaryDirectory() as tmpdir:
        df = pd.DataFrame({
            "num_a": [10, 20, 30, 40, 50],
            "num_b": [5, 15, 25, 35, 45],
            "cat_c": ["cat1", "cat2", "cat1", "cat2", "cat3"]
        })
        generate_visualizations(df, tmpdir)
        files = os.listdir(tmpdir)
        assert "num_a_histogram.png" in files
        assert "cat_c_bar.png" in files
        assert "heatmap.png" in files
