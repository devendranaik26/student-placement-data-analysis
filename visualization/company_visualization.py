
import matplotlib.pyplot as plt
from pathlib import Path

from analysis.company_analysis import analyze_companies


# Output folder
OUTPUT_DIR = Path("visualization/charts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Modern blue and cyan dashboard theme
BACKGROUND_COLOR = "#F8FAFC"
TEXT_COLOR = "#0F172A"
GRID_COLOR = "#E2E8F0"

COMPANY_COLORS = [
    "#2563EB",  # Blue
    "#06B6D4",  # Cyan
    "#0D9488",  # Teal
    "#38BDF8",  # Sky blue
    "#6366F1",  # Indigo
    "#14B8A6",  # Turquoise
    "#3B82F6",  # Bright blue
    "#0891B2",  # Deep cyan
    "#818CF8",  # Soft indigo
    "#67E8F9",  # Light cyan
]


def style_axis(ax):
    """Apply consistent dashboard styling."""
    ax.set_facecolor(BACKGROUND_COLOR)
    ax.grid(axis="y", linestyle="--", alpha=0.8, color=GRID_COLOR)
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID_COLOR)
    ax.spines["bottom"].set_color(GRID_COLOR)

    ax.tick_params(axis="x", colors=TEXT_COLOR)
    ax.tick_params(axis="y", colors=TEXT_COLOR)

    ax.title.set_color(TEXT_COLOR)
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_color(TEXT_COLOR)


def plot_company_placements():
    """Create a chart of students placed by company."""
    df = analyze_companies()

    if df is None or df.empty:
        print("No company placement data available.")
        return

    df = df.sort_values("students_placed", ascending=False).head(10)

    colors = [
        COMPANY_COLORS[i % len(COMPANY_COLORS)]
        for i in range(len(df))
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BACKGROUND_COLOR)

    bars = ax.bar(
        df["company"].astype(str),
        df["students_placed"],
        color=colors,
        edgecolor="#1D4ED8",
        linewidth=0.8,
        width=0.65
    )

    ax.set_title(
        "Company-wise Student Placements",
        fontsize=16,
        fontweight="bold",
        pad=18
    )
    ax.set_xlabel("Company", fontsize=11, labelpad=10)
    ax.set_ylabel("Number of Students Placed", fontsize=11, labelpad=10)

    style_axis(ax)

    ax.bar_label(bars, padding=4, fontsize=10, color=TEXT_COLOR)
    ax.margins(y=0.15)

    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()

    output_path = OUTPUT_DIR / "company_placements.png"
    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
        facecolor=fig.get_facecolor()
    )
    plt.close(fig)

    print(f"Company placement chart saved to: {output_path}")


if __name__ == "__main__":
    plot_company_placements()
