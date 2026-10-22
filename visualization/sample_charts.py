
import os
import pandas as pd
import matplotlib.pyplot as plt

# Create the charts folder
os.makedirs("visualization/charts", exist_ok=True)

# Sample placement data for demonstration
data = {
    "department": ["CSE", "AIML", "ECE", "EEE", "CIVIL"],
    "total_students": [120, 100, 90, 80, 70],
    "placed_students": [105, 92, 68, 55, 42],
    "average_package": [8.5, 9.2, 6.0, 5.2, 4.5]
}

df = pd.DataFrame(data)

# Calculate placement rate
df["placement_rate"] = (
    df["placed_students"] / df["total_students"] * 100
)

# Chart 1: Department-wise placement rate
plt.figure(figsize=(9, 5))
plt.bar(df["department"], df["placement_rate"])
plt.title("Department-wise Placement Rate")
plt.xlabel("Department")
plt.ylabel("Placement Rate (%)")
plt.tight_layout()
plt.savefig("visualization/charts/department_placement_rate.png")
plt.close()

# Chart 2: Students placed by department
plt.figure(figsize=(9, 5))
plt.bar(df["department"], df["placed_students"])
plt.title("Students Placed by Department")
plt.xlabel("Department")
plt.ylabel("Number of Students Placed")
plt.tight_layout()
plt.savefig("visualization/charts/department_student_comparison.png")
plt.close()

# Chart 3: Average package by department
plt.figure(figsize=(9, 5))
plt.bar(df["department"], df["average_package"])
plt.title("Average Package by Department")
plt.xlabel("Department")
plt.ylabel("Average Package (LPA)")
plt.tight_layout()
plt.savefig("visualization/charts/average_package_by_department.png")
plt.close()

print("Sample charts generated successfully!")
print("Check the visualization/charts folder.")
print("Note: These charts use sample data, not actual college records.")

# Chart 4: Salary Package Distribution

package_data = [
    3.5, 4.0, 4.5, 5.0, 5.5,
    6.0, 6.5, 7.0, 7.5, 8.0,
    8.5, 9.0, 10.0, 12.0, 15.0,
    4.2, 5.8, 6.8, 8.2, 11.0
]

plt.figure(figsize=(9, 5))

plt.hist(
    package_data,
    bins=6,
    edgecolor="black"
)

plt.title("Salary Package Distribution")
plt.xlabel("Salary Package (LPA)")
plt.ylabel("Number of Students")

plt.tight_layout()

plt.savefig(
    "visualization/charts/package_distribution.png"
)

plt.close()

print("Package distribution chart generated!")

# Chart 5: Company-Wise Placements

companies = [
    "TCS",
    "Infosys",
    "Wipro",
    "Accenture",
    "Cognizant",
    "Amazon"
]

students_hired = [25, 20, 15, 18, 12, 8]

plt.figure(figsize=(10, 6))

bars = plt.barh(
    companies,
    students_hired,
    color="skyblue",
    edgecolor="black"
)

# Display the number of students on each bar
for bar in bars:
    width = bar.get_width()

    plt.text(
        width + 0.3,
        bar.get_y() + bar.get_height() / 2,
        int(width),
        va="center"
    )

plt.title(
    "Company-Wise Student Placements",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Number of Students Hired", fontsize=12)
plt.ylabel("Company", fontsize=12)

plt.grid(axis="x", linestyle="--", alpha=0.4)

plt.tight_layout()

plt.savefig(
    "visualization/charts/company_placements_sample.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Professional company-wise chart generated!")