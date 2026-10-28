
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

from analysis.package_analysis import analyze_packages


CHART_DIR = Path(__file__).parent / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)


# Blue and cyan dashboard theme
BACKGROUND = "#F8FAFC"
TEXT_COLOR = "#0F172A"
GRID_COLOR = "#E2E8F0"

# Different colors for each department
DEPARTMENT_COLORS = [
    "#2563EB",  # Blue
    "#06B6D4",  # Cyan
    "#0D9488",  # Teal
    "#38BDF8",  # Sky blue
    "#6366F1",  # Indigo
]

BAR_BORDER = "#1D4ED8"

# Package distribution colors
HISTOGRAM_COLOR = "#06B6D4"
HISTOGRAM_BORDER = "#0891B2"


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


def get_package_data():
    """Retrieve and validate actual package data."""
    df = analyze_packages()

    if df is None or df.empty:
        print("No package data available.")
        return None

    required = {"department", "package_lpa"}

    if not required.issubset(df.columns):
        print("Required package columns are missing.")
        return None

    df = df.copy()

    df["package_lpa"] = pd.to_numeric(
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

    colors = [
        DEPARTMENT_COLORS[i % len(DEPARTMENT_COLORS)]
        for i in range(len(averages))
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BACKGROUND)

    bars = ax.bar(
        averages.index.astype(str),
        averages.values,
        color=colors,
        edgecolor=BAR_BORDER,
        linewidth=0.8,
        width=0.62,
        zorder=3
    )

    ax.set_title(
        "Average Salary Package by Department",
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
        "Average Package (LPA)",
        fontsize=11,
        color=TEXT_COLOR,
        labelpad=10
    )

    max_value = float(averages.max())
    ax.set_ylim(0, max_value * 1.18 if max_value > 0 else 1)

    style_axis(ax)

    for bar in bars:
        height = bar.get_height()

        ax.annotate(
            f"{height:.2f}",
            (bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            fontsize=10,
            fontweight="bold",
            color=TEXT_COLOR
        )

    fig.tight_layout()

    output = CHART_DIR / "average_package_by_department.png"

    fig.savefig(
        output,
        dpi=300,
        bbox_inches="tight",
        facecolor=fig.get_facecolor()
    )

    plt.close(fig)
    print(f"Saved: {output}")


def plot_package_distribution():
    """Plot the distribution of salary packages."""
    df = get_package_data()

    if df is None:
        return

    fig, ax = plt.subplots(figsize=(9, 6))
    fig.patch.set_facecolor(BACKGROUND)

    
    counts, bin_edges, patches = ax.hist(
        df["package_lpa"],
        bins=10,
        edgecolor="#1D4ED8",
        linewidth=1.2,
        alpha=0.98,
        zorder=3
    )

    # Different blue and cyan color for each bin
    histogram_colors = [
        "#1D4ED8",  # Deep blue
        "#2563EB",  # Blue
        "#3B82F6",  # Bright blue
        "#0EA5E9",  # Sky blue
        "#06B6D4",  # Cyan
        "#0891B2",  # Deep cyan
        "#0D9488",  # Teal
        "#14B8A6",  # Turquoise
        "#6366F1",  # Indigo
        "#38BDF8",  # Light blue
    ]

    for i, patch in enumerate(patches):
        patch.set_facecolor(
            histogram_colors[i % len(histogram_colors)]
        )


    ax.set_title(
        "Distribution of Salary Packages",
        fontsize=16,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=18
    )

    ax.set_xlabel(
        "Salary Package (LPA)",
        fontsize=11,
        color=TEXT_COLOR,
        labelpad=10
    )

    ax.set_ylabel(
        "Number of Placement Records",
        fontsize=11,
        color=TEXT_COLOR,
        labelpad=10
    )

    style_axis(ax)

    fig.tight_layout()

    output = CHART_DIR / "package_distribution.png"

    fig.savefig(
        output,
        dpi=300,
        bbox_inches="tight",
        facecolor=fig.get_facecolor()
    )

    plt.close(fig)
    print(f"Saved: {output}")


if __name__ == "__main__":
    plot_average_package_by_department()
    plot_package_distribution()
