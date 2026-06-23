
import pandas as pd

def clean_dataset(df):

    df = df.copy()

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Remove completely empty columns
    df.dropna(
        axis=1,
        how="all",
        inplace=True
    )

    numeric_cols = (
        df.select_dtypes(
            include="number"
        ).columns
    )

    categorical_cols = (
        df.select_dtypes(
            exclude="number"
        ).columns
    )

    for col in numeric_cols:

        df[col] = df[col].fillna(
            df[col].median()
        )

    for col in categorical_cols:

        if not df[col].mode().empty:

            df[col] = df[col].fillna(
                df[col].mode()[0]
            )

    return df
