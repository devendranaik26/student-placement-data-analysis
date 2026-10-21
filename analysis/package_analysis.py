
import pandas as pd
import numpy as np
from .database import get_connection


def analyze_packages():
    connection = get_connection()

    if connection is None:
        return None

    try:
        query = """
        SELECT
            s.department,
            p.company,
            p.job_role,
            p.package_lpa
        FROM students s
        JOIN placements p
            ON s.student_id = p.student_id
        WHERE p.package_lpa IS NOT NULL
        """

        package_df = pd.read_sql(query, connection)

        if package_df.empty:
            print("No salary package data available.")
            return package_df

        print("\nOverall Package Statistics (LPA)")
        print("Average:", round(np.mean(package_df["package_lpa"]), 2))
        print("Median:", round(np.median(package_df["package_lpa"]), 2))
        print("Minimum:", np.min(package_df["package_lpa"]))
        print("Maximum:", np.max(package_df["package_lpa"]))

        department_packages = (
            package_df.groupby("department")["package_lpa"]
            .agg(["mean", "median", "min", "max"])
            .round(2)
        )

        print("\nDepartment-wise Package Statistics:")
        print(department_packages)

        return package_df

    finally:
        connection.close()
