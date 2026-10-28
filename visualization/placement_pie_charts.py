
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from analysis.database import get_connection


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHART_DIR = PROJECT_ROOT / "visualization" / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

# Modern dashboard theme
BG = "#F8FAFC"
TEXT = "#0F172A"
MUTED = "#64748B"
GRID = "#E2E8F0"

COLORS = [
    "#2563EB",
    "#06B6D4",
    "#14B8A6",
    "#6366F1",
    "#8B5CF6",
    "#F59E0B",
]


def fetch_data(query):
    connection = get_connection()
    try:
        return pd.read_sql(query, connection)
    finally:
        connection.close()


def create_placement_status_pie():
    query = """
        SELECT
            (SELECT COUNT(*) FROM students) AS total_students,
            (
                SELECT COUNT(DISTINCT student_id)
                FROM placements
                WHERE LOWER(TRIM(status)) IN ('placed', 'selected')
            ) AS placed_students
    """

    df = fetch_data(query)

    total = int(df.loc[0, "total_students"])
    placed = int(df.loc[0, "placed_students"])
    unplaced = max(total - placed, 0)

    if total == 0:
        print("No students found.")
        return

    values = [placed, unplaced]
    labels = ["Placed", "Unplaced"]
    colors = ["#2563EB", "#CBD5E1"]

    fig, ax = plt.subplots(figsize=(9, 7), facecolor=BG)
    ax.set_facecolor(BG)

    wedges, _, percentages = ax.pie(
        values,
        colors=colors,
        startangle=90,
        counterclock=False,
        autopct=lambda pct: f"{pct:.1f}%" if pct > 0 else "",
        pctdistance=0.78,
        explode=(0.035, 0.015),
        shadow=True,
        wedgeprops={
            "width": 0.38,
            "edgecolor": "white",
            "linewidth": 3,
        },
        textprops={
            "color": "white",
            "fontsize": 12,
            "fontweight": "bold",
        },
    )

    # Centre of the doughnut
    ax.text(
        0, 0.10, f"{total}",
        ha="center", va="center",
        fontsize=28, fontweight="bold", color=TEXT,
    )
    ax.text(
        0, -0.16, "TOTAL STUDENTS",
        ha="center", va="center",
        fontsize=9, fontweight="bold", color=MUTED,
    )

    ax.set_title(
        "Placement Status Overview",
        fontsize=19,
        fontweight="bold",
        color=TEXT,
        pad=24,
    )

    ax.legend(
        wedges,
        [f"{label}: {value}" for label, value in zip(labels, values)],
        title="Student Status",
        loc="lower center",
        bbox_to_anchor=(0.5, -0.08),
        ncol=2,
        frameon=False,
        fontsize=10,
        labelcolor=TEXT,
    )

    fig.text(
        0.5, 0.025,
        "Student Placement Data Analysis System",
        ha="center", fontsize=9, color=MUTED,
    )

    fig.tight_layout()
    fig.savefig(
        CHART_DIR / "placement_status_pie.png",
        dpi=300,
        facecolor=BG,
        bbox_inches="tight",
    )
    plt.close(fig)

    print("Created: placement_status_pie.png")


def create_company_distribution_pie():
    query = """
        SELECT
            company,
            COUNT(DISTINCT student_id) AS placement_count
        FROM placements
        WHERE LOWER(TRIM(status)) IN ('placed', 'selected')
        GROUP BY company
        ORDER BY placement_count DESC, company
    """

    df = fetch_data(query)
    df = df.dropna(subset=["company"])
    df = df[df["placement_count"] > 0]

    if df.empty:
        print("No qualifying company placements found.")
        return

    values = df["placement_count"].tolist()
    labels = df["company"].astype(str).tolist()
    colors = [COLORS[i % len(COLORS)] for i in range(len(labels))]

    fig, ax = plt.subplots(figsize=(10, 7), facecolor=BG)
    ax.set_facecolor(BG)

    wedges, _, _ = ax.pie(
        values,
        colors=colors,
        startangle=90,
        counterclock=False,
        autopct=lambda pct: f"{pct:.1f}%" if pct >= 4 else "",
        pctdistance=0.78,
        explode=[0.025] * len(values),
        shadow=True,
        wedgeprops={
            "width": 0.40,
            "edgecolor": "white",
            "linewidth": 2.5,
        },
        textprops={
            "color": "white",
            "fontsize": 10,
            "fontweight": "bold",
        },
    )

    total_placements = sum(values)

    ax.text(
        0, 0.10, f"{total_placements}",
        ha="center", va="center",
        fontsize=25, fontweight="bold", color=TEXT,
    )
    ax.text(
        0, -0.16, "PLACEMENTS",
        ha="center", va="center",
        fontsize=9, fontweight="bold", color=MUTED,
    )

    ax.set_title(
        "Company-wise Placement Distribution",
        fontsize=18,
        fontweight="bold",
        color=TEXT,
        pad=24,
    )

    ax.legend(
        wedges,
        [
            f"{company}  •  {count}"
            for company, count in zip(labels, values)
        ],
        title="Company  •  Students",
        loc="center left",
        bbox_to_anchor=(1.00, 0.5),
        frameon=False,
        fontsize=10,
        labelcolor=TEXT,
    )

    fig.text(
        0.5, 0.025,
        "Student Placement Data Analysis System",
        ha="center", fontsize=9, color=MUTED,
    )

    fig.tight_layout()
    fig.savefig(
        CHART_DIR / "company_distribution_pie.png",
        dpi=300,
        facecolor=BG,
        bbox_inches="tight",
    )
    plt.close(fig)

    print("Created: company_distribution_pie.png")


if __name__ == "__main__":
    create_placement_status_pie()
    create_company_distribution_pie()
