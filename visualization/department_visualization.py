import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from pathlib import Path

from analysis.department_analysis import analyze_departments


CHART_DIR = Path(__file__).parent / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)


def plot_department_placement_rate():
    """Plot placement percentage for each department."""

    df = analyze_departments()

    if df is None or df.empty:
        print("No department data available.")
        return

    required = {"department", "placement_rate"}

    if not required.issubset(df.columns):
        print("Required department placement columns are missing.")
        return

    df = df.dropna(subset=["department", "placement_rate"])

    if df.empty:
        print("No valid placement-rate data available.")
        return

    plt.figure(figsize=(10, 6))

    bars = plt.bar(
        df["department"].astype(str),
        df["placement_rate"]
    )

    plt.title("Department-wise Placement Rate")
    plt.xlabel("Department")
    plt.ylabel("Placement Rate (%)")
    plt.xticks(rotation=30, ha="right")
    plt.ylim(0, max(100, float(df["placement_rate"].max()) * 1.15))

    for bar in bars:
        height = bar.get_height()
        plt.annotate(
            f"{height:.1f}%",
            (bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center"
        )

    plt.tight_layout()

    output = CHART_DIR / "department_placement_rate.png"
    plt.savefig(output, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved: {output}")


def plot_department_student_comparison():
    """Compare total and placed students by department."""

    df = analyze_departments()

    if df is None or df.empty:
        print("No department data available.")
        return

    required = {"department", "total_students", "placed_students"}

    if not required.issubset(df.columns):
        print("Required student comparison columns are missing.")
        return

    df = df.dropna(
        subset=["department", "total_students", "placed_students"]
    )

    if df.empty:
        print("No valid student comparison data available.")
        return

    positions = list(range(len(df)))
    width = 0.36

    plt.figure(figsize=(10, 6))

    plt.bar(
        [p - width / 2 for p in positions],
        df["total_students"],
        width=width,
        label="Total Students"
    )

    plt.bar(
        [p + width / 2 for p in positions],
        df["placed_students"],
        width=width,
        label="Placed Students"
    )

    plt.title("Total Students vs. Placed Students by Department")
    plt.xlabel("Department")
    plt.ylabel("Number of Students")

    plt.xticks(
        positions,
        df["department"].astype(str),
        rotation=30,
        ha="right"
    )

    plt.legend()
    plt.tight_layout()

    output = CHART_DIR / "department_student_comparison.png"
    plt.savefig(output, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved: {output}")


if __name__ == "__main__":
    plot_department_placement_rate()
    plot_department_student_comparison()

