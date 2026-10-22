
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from pathlib import Path
from analysis.database import get_connection


CHART_DIR = Path(__file__).parent / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)


def get_skills_data():
    """Retrieve skill demand counts from the skills table."""

    connection = get_connection()

    if connection is None:
        print("Database unavailable. Cannot create skills chart.")
        return None

    try:
        # Replace these table/column names with your actual schema.
        query = """
        SELECT
            skill_name,
            demand_count
        FROM skills
        WHERE skill_name IS NOT NULL
          AND demand_count IS NOT NULL
        ORDER BY demand_count DESC
        LIMIT 10
        """

        df = pd.read_sql(query, connection)

        if df.empty:
            print("No skills demand data available.")
            return None

        return df

    except Exception as error:
        print(
            "Skills chart could not be generated. "
            "Check the actual skills table and column names."
        )
        print(f"Database query error: {error}")
        return None

    finally:
        connection.close()


def plot_top_demand_skills():
    """Plot the most frequently demanded skills."""

    df = get_skills_data()

    if df is None or df.empty:
        return

    df = df.sort_values("demand_count", ascending=True)

    plt.figure(figsize=(10, 6))

    plt.barh(
        df["skill_name"].astype(str),
        df["demand_count"]
    )

    plt.title("Top 10 In-Demand Skills")
    plt.xlabel("Demand Count")
    plt.ylabel("Skill")

    plt.tight_layout()

    output = CHART_DIR / "top_demand_skills.png"
    plt.savefig(output, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved: {output}")


if __name__ == "__main__":
    plot_top_demand_skills()

