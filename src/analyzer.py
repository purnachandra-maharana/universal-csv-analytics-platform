
import pandas as pd

def dataset_summary(df):

    summary = {

        "Rows":
        int(df.shape[0]),

        "Columns":
        int(df.shape[1]),

        "Missing Values":
        int(df.isnull().sum().sum()),

        "Duplicates":
        int(df.duplicated().sum())

    }

    return summary


def missing_values(df):

    return (
        df.isnull()
        .sum()
        .sort_values(
            ascending=False
        )
    )


def correlation_matrix(df):

    return df.corr(
        numeric_only=True
    )
