
import pandas as pd

def detect_columns(df):

    numeric_cols = list(
        df.select_dtypes(
            include="number"
        ).columns
    )

    categorical_cols = list(
        df.select_dtypes(
            include="object"
        ).columns
    )

    return {
        "numeric": numeric_cols,
        "categorical": categorical_cols
    }
