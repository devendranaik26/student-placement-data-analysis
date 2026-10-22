
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from pathlib import Path

from analysis.package_analysis import analyze_packages


CHART_DIR = Path(__file__).parent / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)


def get_package_data():
    """Retrieve and validate package data."""

    df = analyze_packages()

    if df is None or df.empty:
        print("No package data available.")
        return None

    required = {"department", "package_lpa"}

    if not required.issubset(df.columns):
        print("Required package columns are missing.")
        return None

    df = df.copy()
    df["package_lpa"] = __import__("pandas").to_numeric(
        df["package_lpa"],
        errors="coerce"
    )

    df = df.dropna(subset=["department", "package_lpa"])

    if df.empty:
        print("No valid package values available.")
        return None

    return df


def plot_average_package_by_department():
    """Plot average salary package by department."""

    df = get_package_data()

    if df is None:
        return

    averages = (
        df.groupby("department")["package_lpa"]
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 6))

    bars = plt.bar(
        averages.index.astype(str),
        averages.values
    )

    plt.title("Average Salary Package by Department")
    plt.xlabel("Department")
    plt.ylabel("Average Package (LPA)")
    plt.xticks(rotation=30, ha="right")

    for bar in bars:
        height = bar.get_height()
        plt.annotate(
            f"{height:.2f}",
            (bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center"
        )

    plt.tight_layout()

    output = CHART_DIR / "average_package_by_department.png"
    plt.savefig(output, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved: {output}")


def plot_package_distribution():
    """Plot the distribution of salary packages."""

    df = get_package_data()

    if df is None:
        return

    plt.figure(figsize=(9, 6))

    plt.hist(
        df["package_lpa"],
        bins=10,
        edgecolor="black"
    )

    plt.title("Distribution of Salary Packages")
    plt.xlabel("Salary Package (LPA)")
    plt.ylabel("Number of Placement Records")

    plt.tight_layout()

    output = CHART_DIR / "package_distribution.png"
    plt.savefig(output, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved: {output}")


if __name__ == "__main__":
    plot_average_package_by_department()
    plot_package_distribution()

