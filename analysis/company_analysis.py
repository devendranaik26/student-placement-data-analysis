
import pandas as pd
from database import get_connection


def analyze_companies():
    connection = get_connection()

    if connection is None:
        return None

    try:
        query = """
        SELECT
            company,
            COUNT(DISTINCT student_id) AS students_placed,
            ROUND(AVG(package_lpa), 2) AS average_package_lpa,
            ROUND(MAX(package_lpa), 2) AS highest_package_lpa
        FROM placements
        WHERE status = 'Placed'
        GROUP BY company
        ORDER BY students_placed DESC
        """

        company_df = pd.read_sql(query, connection)

        print("\nCompany-wise Placement Analysis:")
        print(company_df.to_string(index=False))

        return company_df

    finally:
        connection.close()
