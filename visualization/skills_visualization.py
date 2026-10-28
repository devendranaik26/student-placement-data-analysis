
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from pathlib import Path

from analysis.skills_analysis import analyze_skills


CHART_DIR = Path(__file__).parent / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)


# Blue and cyan dashboard theme
BACKGROUND = "#F8FAFC"
TEXT_COLOR = "#0F172A"
GRID_COLOR = "#E2E8F0"

# Different colors for each skill bar
SKILL_COLORS = [
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


def plot_top_demand_skills():
    """Plot skills ranked by the number of placed students."""

    df = analyze_skills()

    if df is None or df.empty:
        print("No skills data available.")
        return

    required = {
        "skill_name",
        "placed_students_with_skill"
    }

    if not required.issubset(df.columns):
        print("Required skills analysis columns are missing.")
        return

    df = df.dropna(
        subset=["skill_name", "placed_students_with_skill"]
    ).copy()

    df["placed_students_with_skill"] = (
        df["placed_students_with_skill"].astype(float)
    )

    df = df.nlargest(10, "placed_students_with_skill")
    df = df.sort_values("placed_students_with_skill")

    if df.empty:
        print("No valid skills data available.")
        return

    # Assign a different color to each skill
    colors = [
        SKILL_COLORS[i % len(SKILL_COLORS)]
        for i in range(len(df))
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)

    bars = ax.barh(
        df["skill_name"].astype(str),
        df["placed_students_with_skill"],
        color=colors,
        edgecolor="#1D4ED8",
        linewidth=0.8,
        height=0.65,
        zorder=3
    )

    # Chart title and labels
    ax.set_title(
        "Top 10 Skills by Number of Placed Students",
        fontsize=16,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=18
    )

    ax.set_xlabel(
        "Number of Placed Students with Skill",
        fontsize=11,
        color=TEXT_COLOR,
        labelpad=10
    )

    ax.set_ylabel(
        "Skill",
        fontsize=11,
        color=TEXT_COLOR,
        labelpad=10
    )

    # Dashboard styling
    ax.set_axisbelow(True)
    ax.grid(
        axis="x",
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

    # Display values at the end of each bar
    ax.bar_label(
        bars,
        padding=5,
        fontsize=10,
        fontweight="bold",
        color=TEXT_COLOR
    )

    ax.margins(x=0.15)
    fig.tight_layout()

    output = CHART_DIR / "top_demand_skills.png"

    fig.savefig(
        output,
        dpi=300,
        bbox_inches="tight",
        facecolor=fig.get_facecolor()
    )

    plt.close(fig)
    print(f"Saved: {output}")


if __name__ == "__main__":
    plot_top_demand_skills()
