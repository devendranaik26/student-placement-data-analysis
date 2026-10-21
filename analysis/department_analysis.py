
import pandas as pd
from .database import get_connection


def analyze_departments():
    connection = get_connection()

    if connection is None:
        return None

    try:
        query = """
        SELECT
            s.department,
            COUNT(DISTINCT s.student_id) AS total_students,
            COUNT(DISTINCT p.student_id) AS placed_students
        FROM students s
        LEFT JOIN placements p
            ON s.student_id = p.student_id
        GROUP BY s.department
        ORDER BY placed_students DESC
        """

        placement_df = pd.read_sql(query, connection)

        placement_df["placement_rate"] = (
            placement_df["placed_students"]
            / placement_df["total_students"] * 100
        ).round(2)

        return placement_df

    finally:
        connection.close()
