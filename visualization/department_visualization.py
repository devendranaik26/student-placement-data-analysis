
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from analysis.department_analysis import analyze_departments


CHART_DIR = Path(__file__).parent / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

# Dashboard background and text
BACKGROUND = "#F8FAFC"
TEXT_COLOR = "#172033"
GRID_COLOR = "#DCE2EA"

# Different bright colors for each department
DEPARTMENT_COLORS = {
    "CSE": "#3182CE",   # Blue
    "AIML": "#10B981",  # Green
    "AIDS": "#8B5CF6",  # Purple
    "ECE": "#F59E0B",   # Orange
    "IT": "#F43F5E",    # Pink
}

# Color used if a department name is not in the mapping
DEFAULT_COLOR = "#64748B"

# Total students bars are light gray
TOTAL_COLOR = "#CBD5E1"
TOTAL_BORDER = "#64748B"


def get_department_color(department):
    """Get the assigned color for a department."""
    return DEPARTMENT_COLORS.get(str(department).upper(), DEFAULT_COLOR)


def style_axis(ax):
    """Apply a clean dashboard style."""
    ax.set_facecolor(BACKGROUND)
    ax.set_axisbelow(True)

    ax.grid(
        axis="y",
        linestyle="--",
        linewidth=0.8,
        color=GRID_COLOR,
        alpha=0.9
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(GRID_COLOR)

    ax.tick_params(axis="both", colors=TEXT_COLOR, labelsize=10)
    ax.tick_params(axis="y", length=0)


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

    df = df.dropna(
        subset=["department", "placement_rate"]
    ).copy()

    if df.empty:
        print("No valid placement-rate data available.")
        return

    # Assign a different color to every department bar
    colors = [
        get_department_color(dept)
        for dept in df["department"]
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BACKGROUND)

    bars = ax.bar(
        df["department"].astype(str),
        df["placement_rate"],
        color=colors,
        edgecolor="white",
        linewidth=1.2,
        width=0.62,
        zorder=3
    )

    ax.set_title(
        "Department-wise Placement Rate",
        fontsize=16,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=18
    )

    ax.set_xlabel(
        "Department",
        fontsize=11,
        color=TEXT_COLOR,
        labelpad=10
    )

    ax.set_ylabel(
        "Placement Rate (%)",
        fontsize=11,
        color=TEXT_COLOR,
        labelpad=10
    )

    max_rate = float(df["placement_rate"].max())
    ax.set_ylim(0, max(100, max_rate * 1.15))

    style_axis(ax)

    for bar in bars:
        height = bar.get_height()

        ax.annotate(
            f"{height:.1f}%",
            (bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            fontsize=10,
            fontweight="bold",
            color=TEXT_COLOR
        )

    fig.tight_layout()

    output = CHART_DIR / "department_placement_rate.png"

    fig.savefig(
        output,
        dpi=300,
        bbox_inches="tight",
        facecolor=fig.get_facecolor()
    )

    plt.close(fig)
    print(f"Saved: {output}")


def plot_department_student_comparison():
    """Compare total and placed students by department."""

    df = analyze_departments()

    if df is None or df.empty:
        print("No department data available.")
        return

    required = {
        "department",
        "total_students",
        "placed_students"
    }

    if not required.issubset(df.columns):
        print("Required student comparison columns are missing.")
        return

    df = df.dropna(
        subset=[
            "department",
            "total_students",
            "placed_students"
        ]
    ).copy()

    if df.empty:
        print("No valid student comparison data available.")
        return

    positions = np.arange(len(df))
    width = 0.36

    # Each department gets its own color for placed students
    placed_colors = [
        get_department_color(dept)
        for dept in df["department"]
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BACKGROUND)

    # Light gray bars represent total students
    total_bars = ax.bar(
        positions - width / 2,
        df["total_students"],
        width,
        label="Total Students",
        color=TOTAL_COLOR,
        edgecolor=TOTAL_BORDER,
        linewidth=0.7,
        zorder=3
    )

    # Colorful bars represent placed students
    placed_bars = ax.bar(
        positions + width / 2,
        df["placed_students"],
        width,
        label="Placed Students",
        color=placed_colors,
        edgecolor="white",
        linewidth=1.0,
        zorder=3
    )

    # Show the student counts above both sets of bars
    for bars in (total_bars, placed_bars):
        for bar in bars:
            height = bar.get_height()

            ax.annotate(
                f"{height:g}",
                (bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                fontsize=9,
                fontweight="bold",
                color=TEXT_COLOR
            )

    ax.set_title(
        "Total Students vs. Placed Students by Department",
        fontsize=15,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=18
    )

    ax.set_xlabel(
        "Department",
        fontsize=11,
        color=TEXT_COLOR,
        labelpad=10
    )

    ax.set_ylabel(
        "Number of Students",
        fontsize=11,
        color=TEXT_COLOR,
        labelpad=10
    )

    ax.set_xticks(positions)
    ax.set_xticklabels(df["department"].astype(str))

    max_students = max(
        float(df["total_students"].max()),
        float(df["placed_students"].max())
    )

    ax.set_ylim(
        0,
        max_students * 1.18 if max_students > 0 else 1
    )

    style_axis(ax)

    legend = ax.legend(frameon=False, fontsize=10)

    for label in legend.get_texts():
        label.set_color(TEXT_COLOR)

    fig.tight_layout()

    output = CHART_DIR / "department_student_comparison.png"

    fig.savefig(
        output,
        dpi=300,
        bbox_inches="tight",
        facecolor=fig.get_facecolor()
    )

    plt.close(fig)
    print(f"Saved: {output}")


if __name__ == "__main__":
    plot_department_placement_rate()
    plot_department_student_comparison()
