
import os
import matplotlib.pyplot as plt
import seaborn as sns

def generate_visualizations(df, output_folder):

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    numeric_cols = (
        df.select_dtypes(
            include="number"
        ).columns
    )

    categorical_cols = (
        df.select_dtypes(
            include="object"
        ).columns
    )

    # -------------------------
    # Histograms
    # -------------------------

    for col in numeric_cols:

        try:

            plt.figure(figsize=(8,5))

            df[col].hist()

            plt.title(
                f"Histogram - {col}"
            )

            plt.savefig(
                os.path.join(
                    output_folder,
                    f"{col}_histogram.png"
                )
            )

            plt.close()

        except:
            pass

    # -------------------------
    # Bar Charts
    # -------------------------

    for col in categorical_cols:

        try:

            plt.figure(figsize=(8,5))

            (
                df[col]
                .value_counts()
                .head(10)
                .plot(kind="bar")
            )

            plt.title(
                f"Top Categories - {col}"
            )

            plt.savefig(
                os.path.join(
                    output_folder,
                    f"{col}_bar.png"
                )
            )

            plt.close()

        except:
            pass

    # -------------------------
    # Correlation Heatmap
    # -------------------------

    try:

        corr = df.corr(
            numeric_only=True
        )

        plt.figure(
            figsize=(10,8)
        )

        sns.heatmap(
            corr,
            annot=True,
            cmap="coolwarm"
        )

        plt.title(
            "Correlation Heatmap"
        )

        plt.savefig(
            os.path.join(
                output_folder,
                "heatmap.png"
            )
        )

        plt.close()

    except:
        pass
