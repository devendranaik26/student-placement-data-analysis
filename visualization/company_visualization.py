
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from pathlib import Path
from analysis.database import get_connection


CHART_DIR = Path(__file__).parent / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)


def get_company_data():
    """Retrieve the number of distinct students hired by each company."""

    connection = get_connection()

    if connection is None:
        print("Database unavailable. Cannot create company chart.")
        return None

    try:
        query = """
        SELECT
            p.company,
            COUNT(DISTINCT p.student_id) AS students_hired
        FROM placements p
        WHERE p.company IS NOT NULL
          AND p.company <> ''
        GROUP BY p.company
        ORDER BY students_hired DESC
        """

        df = pd.read_sql(query, connection)

        if df.empty:
            print("No company placement data available.")
            return None

        return df

    except Exception as error:
        print(f"Could not retrieve company data: {error}")
        return None

    finally:
        connection.close()


def plot_company_placements():
    """Create a chart showing students hired by each company."""

    df = get_company_data()

    if df is None or df.empty:
        return

    # Display the top 10 companies to keep the chart readable.
    df = df.head(10).sort_values("students_hired")

    plt.figure(figsize=(10, 6))

    plt.barh(
        df["company"].astype(str),
        df["students_hired"]
    )

    plt.title("Top Companies by Number of Students Hired")
    plt.xlabel("Number of Students Hired")
    plt.ylabel("Company")

    plt.tight_layout()

    output = CHART_DIR / "company_placements.png"
    plt.savefig(output, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved: {output}")


if __name__ == "__main__":
    plot_company_placements()

