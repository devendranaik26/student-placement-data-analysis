
from department_analysis import analyze_departments
from package_analysis import analyze_packages
from company_analysis import analyze_companies
from skills_analysis import analyze_skills


def main():
    print("\n===== STUDENT PLACEMENT DATA ANALYSIS =====")

    print("\n--- Department Analysis ---")
    department_df = analyze_departments()
    if department_df is not None:
        print(department_df.to_string(index=False))

    print("\n--- Package Analysis ---")
    analyze_packages()

    print("\n--- Company Analysis ---")
    analyze_companies()

    print("\n--- Skills Analysis ---")
    analyze_skills()

    print("\n===== ANALYSIS COMPLETED =====")


if __name__ == "__main__":
    main()
