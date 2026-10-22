
from visualization.department_visualization import (
    plot_department_placement_rate,
    plot_department_student_comparison,
)

from visualization.package_visualization import (
    plot_average_package_by_department,
    plot_package_distribution,
)

from visualization.company_visualization import (
    plot_company_placements,
)


def main():
    print("\nStarting Student Placement Visualizations...\n")

    tasks = [
        (
            "Department placement rate",
            plot_department_placement_rate,
        ),
        (
            "Department student comparison",
            plot_department_student_comparison,
        ),
        (
            "Average package by department",
            plot_average_package_by_department,
        ),
        (
            "Package distribution",
            plot_package_distribution,
        ),
        (
            "Company-wise placements",
            plot_company_placements,
        ),
    ]

    for name, function in tasks:
        print(f"\nGenerating: {name}")

        try:
            function()
        except Exception as error:
            print(f"Could not generate {name}: {error}")

    print("\nVisualization process finished.")
    print("Check the visualization/charts folder for generated charts.")


if __name__ == "__main__":
    main()

