
def generate_insights(df):

    insights = []

    insights.append(
        f"Dataset contains {len(df)} rows."
    )

    insights.append(
        f"Dataset contains {df.shape[1]} columns."
    )

    missing = (
        df.isnull()
        .sum()
        .sum()
    )

    insights.append(
        f"Missing values found: {missing}"
    )

    duplicates = (
        df.duplicated()
        .sum()
    )

    insights.append(
        f"Duplicate rows found: {duplicates}"
    )

    return insights
